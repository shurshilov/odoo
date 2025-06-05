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

export class FiasTextField extends TextField {
  static template = xml`
        
        <t t-if="props.readonly">
            <span t-esc="props.value or ''" />
        </t>
        <t t-else="">
            <div t-ref="div">
                <textarea
                    class="o_input"
                    t-att-class="{'o_field_translate': props.isTranslatable}"
                    t-att-id="props.id"
                    t-att-placeholder="props.placeholder"
                    t-att-rows="rowCount"
                    t-on-input="onInput"
                    t-ref="textarea"
                />
            <ul t-if="state.suggestions.length">
                <li class="fias-address-item" t-foreach="state.suggestions" t-as="suggestion" t-key="suggestion" t-on-click="selectSuggestion">
                    <span class="fias-address-item__text" t-esc="suggestion" />
                </li>
            </ul>
                <t t-if="props.isTranslatable">
                    <TranslationButton
                        fieldName="props.name"
                        record="props.record"
                    />
                </t>
            </div>
        </t>
    `;

  setup() {
    super.setup();
    this.state = useState({
      suggestions: [],
    });
    this.onInput = debounce(this.fetchSuggestions.bind(this), 800);
    this.rpc = useService("rpc");
    this.notification = useService("notification");
    onWillStart(this.willStart);
  }

  // Lifecycle
  async willStart() {
    if (!window.fias_api_key) {
      window.fias_api_key = await this.rpc("/web/dataset/call_kw", {
        model: "fias.settings",
        method: "get_api_key",
        kwargs: {},
        args: [],
      });
    }
  }

  async fetchSuggestions(ev) {
    this.props.update(ev.target.value);
    console.log(this);
    console.log(ev.target.value);
    if (ev.target.value) {
      // const url = `https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressHint`;
      // const body = {
      //   addressType: 2,
      //   locationsBoost: "1405113",
      //   searchNonActive: false,
      //   searchString: this.props.value,
      // };
      // const response = await fetch(url, {
      //   method: "POST",
      //   body: JSON.stringify(body),
      //   headers: { "master-token": "bfa2407b-1dc4-4714-9346-b678408eb099" },
      // });
      //           https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressHint?search_string=%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D1%8F%D1%80%D1%81%D0%BA%20%D0%BB%D0%B5%D0%BD%D0%B8%D0%BD%D0%B0&address_type=2
      try {
        const url = `https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressHint?search_string=${ev.target.value}&address_type=2`;
        const response = await fetch(url, {
          headers: { "master-token": window.fias_api_key },
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data);
          this.state.suggestions = data["hints"].map(
            (item) => item["full_name"],
          ); // Или другой нужный вам атрибут
          // this.render();
        } else {
          console.error("Ошибка при получении адресов...");
        }
      } catch (error) {
        console.error("Ошибка при получении адресов:", error);
        this.notification.add("Ошибка при получении адресов", {
          type: "danger",
        });
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

registry.category("fields").add("field_text_fias", FiasTextField);
