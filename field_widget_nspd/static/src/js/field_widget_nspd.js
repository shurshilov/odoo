/** @odoo-module **/

import { registry } from "@web/core/registry";
import { xml } from "@odoo/owl";
import { debounce } from "@web/core/utils/timing";
import { CharField } from "@web/views/fields/char/char_field";
import { TextField } from "@web/views/fields/text/text_field";
import { useService } from "@web/core/utils/hooks";
const { onWillStart, useState } = owl;

// export class FieldCharFias extends CharField {
//   //         <input type="text" t-model="address" t-on-input="onInput" placeholder="Введите адрес"/>
//   static template = xml`

//         <div>
//               <t t-if="props.readonly">
//                 <span t-esc="formattedValue" />
//             </t>
//             <t t-else="">
//                 <input
//                     class="o_input"
//                     t-att-class="{'o_field_translate': props.isTranslatable}"
//                     t-att-id="props.id"
//                     t-att-type="props.isPassword ? 'password' : 'text'"
//                     t-att-autocomplete="props.autocomplete or (props.isPassword ? 'new-password' : 'off')"
//                     t-att-maxlength="props.maxLength > 0 and props.maxLength"
//                     t-att-placeholder="props.placeholder"
//                     t-ref="input"
//                     t-on-input="onInput"
//                 />
//             <ul t-if="suggestions.length">
//                 <li t-foreach="suggestions" t-as="suggestion" t-key="suggestion" t-on-click="selectSuggestion">
//                     <span t-esc="suggestion" />
//                 </li>
//             </ul>
//                 <t t-if="props.isTranslatable">
//                     <TranslationButton
//                         fieldName="props.name"
//                         record="props.record"
//                     />
//                 </t>
//             </t>

//         </div>
//     `;

//   setup() {
//     this.address = "";
//     this.suggestions = [];
//     this.onInput = debounce(this.fetchSuggestions, 300);
//   }

//   async fetchSuggestions() {
//     if (this.address) {
//       const url = `https://fias.nalog.ru/WebAPI/Address.svc/GetSuggestions?Address=${this.address}`;
//       const response = await fetch(url);
//       if (response.ok) {
//         const data = await response.json();
//         this.suggestions = data.map((item) => item.FullAddress); // Или другой нужный вам атрибут
//         this.render();
//       } else {
//         console.error("Ошибка при получении адресов");
//       }
//     } else {
//       this.suggestions = [];
//       this.render();
//     }
//   }

//   selectSuggestion(event) {
//     this.address = event.target.innerText;
//     this.suggestions = [];
//     this.render();
//   }
// }

// registry.category("fields").add("field_char_fias", FieldCharFias);

export class NspdTextField extends TextField {
  setup() {
    super.setup();
    this.state = useState({
      suggestions: [],
    });
    this.onInput = debounce(this.fetchSuggestions.bind(this), 300);
    this.rpc = useService("rpc");
    // onWillStart(this.willStart);
  }

  // Lifecycle
  // async willStart() {
  //   if (!window.fias_api_key) {
  //     window.fias_api_key = await this.rpc("/web/dataset/call_kw", {
  //       model: "fias.settings",
  //       method: "get_api_key",
  //       kwargs: {},
  //       args: [],
  //     });
  //   }
  // }

  async fetchSuggestions(ev) {
    this.props.update(ev.target.value);
    console.log(this);
    console.log(ev.target.value);
    if (ev.target.value) {
      // {
      //     "title": "Земельные участки из ЕГРН",
      //     "layerTreeId": 72,
      //     "layerId": 36048,
      //     "layerType": "wms",
      //     "geometryType": "POLYGON",
      //     "layerName": "Росреестр: Земельные участки ЕГРН",
      //     "layerVisibleByDefault": False,
      //     "categoryId": 36368,
      // }
      // base_url = (
      //     "https://nspd.gov.ru" if not self._dns_resolve else "https://2.63.246.76"
      // )
      // return Client(
      //     base_url=base_url,
      //     timeout=self._timeout,
      //     headers={
      //         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
      //         "Referer": "https://nspd.gov.ru",
      //         "Host": "nspd.gov.ru",
      //     },
      const params = {
        query: ev.target.value,
        layersId: 36048,
      };
      const url = "https://nspd.gov.ru/api/geoportal/v2/search/geoportal";
      const response = await fetch(url, {
        params: params,
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
          Referer: "https://nspd.gov.ru",
          Host: "nspd.gov.ru",
        },
      });
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        // this.state.suggestions = data["hints"].map((item) => item["full_name"]); // Или другой нужный вам атрибут
        // this.render();
      } else {
        console.error("Ошибка при получении адресов");
      }
    } else {
      this.state.suggestions = [];
      // this.render();
    }
  }

  selectSuggestion(event) {
    this.props.update(event.target.innerText);
    this.state.suggestions = [];
    // this.render();
  }
}

registry.category("fields").add("field_text_nspd", NspdTextField);
