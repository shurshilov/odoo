/** @odoo-module **/

import { registry } from "@web/core/registry";
import { xml } from "@odoo/owl";
import { CharField } from "@web/views/fields/char/char_field";
import { TextField } from "@web/views/fields/text/text_field";
import { useService } from "@web/core/utils/hooks";
const { onMounted, useState } = owl;

export class FieldCharNspd extends CharField {
  static template = xml`
        <t t-call="web.CharField"/>
        <div class="btn-group" role="group">
            <button 
                type="button" 
                class="btn btn-primary btn-sm"
                t-on-click="fetchSuggestions"
                t-att-disabled="!props.value || this.state.cadastr == this.props.value">
                <i class="fa fa-hand-o-up me-1"></i>
                Получить адрес и координаты из НСПД
            </button>
        </div>
        <ul t-if="state.suggestions.length">
            <li class="fias-address-item" t-foreach="state.suggestions" t-as="suggestion" t-key="suggestion" t-on-click="selectSuggestion">
                <span class="fias-address-item__text" t-esc="suggestion" />
            </li>
        </ul>
    `;

  setup() {
    super.setup();
    this.state = useState({
      suggestions: [],
      cadastr: this.props.value || "",
    });
    this.rpc = useService("rpc");
    this.notification = useService("notification");
    onMounted(this.onMounted);
  }

  // async inputListener(ev) {
  //   if (ev.target === this.input.el) {
  //     const debounce_fetch = debounce(this.fetchSuggestions.bind(this), 800);
  //     await debounce_fetch(ev);
  //   }
  // }
  // onMounted() {
  //   this.input.el.addEventListener("input", this.inputListener.bind(this));
  // }

  coordEPSG3857ToWGS84(coord) {
    const x = coord[0];
    const y = coord[1];
    const R = 6378137; // Радиус Земли в метрах
    const lon = (x / R) * (180 / Math.PI);
    const lat =
      (2 * Math.atan(Math.exp(y / R)) - Math.PI / 2) * (180 / Math.PI);
    return [lat, lon];
  }

  async fetchSuggestions(ev) {
    if (this.props.value) {
      try {
        this.state.cadastr = this.props.value;
        const params = {
          query: this.props.value,
          // "Сооружения" 36328
          // "Здания" 36049
          layersId: 36049,
          // "Земельные участки из ЕГРН" 36048
          // layersId: 36048,
        };
        const urlParams = new URLSearchParams(params).toString();
        const url = "https://nspd.gov.ru/api/geoportal/v2/search/geoportal?";
        const response = await fetch(url + urlParams, {
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
          const address =
            data["data"]["features"][0]["properties"]["options"][
              "readable_address"
            ];
          // EPSG:3857
          const coords = this.coordEPSG3857ToWGS84(
            data["data"]["features"][0]["geometry"]["coordinates"][0][0],
          );
          const values = {};
          values[this.props.fieldNameAddress] = address;
          values[this.props.fieldNameLat] = coords[0];
          values[this.props.fieldNameLng] = coords[1];
          await this.props.record.update(values);
        } else {
          throw "Ошибка при получении адресов";
        }
      } catch (error) {
        console.error("Ошибка при получении адреса НСПД:", error);
        this.notification.add(
          "Ошибка при получении адреса НСПД, попробуйте снова",
          {
            type: "danger",
          },
        );
      }
    } else {
      this.state.suggestions = [];
    }
  }

  selectSuggestion(event) {
    this.props.update(event.target.innerText);
    this.state.suggestions = [];
  }
}
// добавить возможность установить любое поле
FieldCharNspd.props = {
  ...CharField.props,
  fieldNameAddress: { type: String, optional: true },
  fieldNameLat: { type: String, optional: true },
  fieldNameLng: { type: String, optional: true },
};
FieldCharNspd.extractProps = ({ attrs, field }) => ({
  ...CharField.extractProps({ attrs, field }),
  fieldNameLat: attrs.options.field_name_lat || "geo_latitude",
  fieldNameLng: attrs.options.field_name_lng || "geo_longitude",
  fieldNameAddress: attrs.options.field_name_address || "geo_address",
});
registry.category("fields").add("field_char_nspd", FieldCharNspd);

// export class NspdTextField extends TextField {
//   static template = xml`
//         <t t-call="web.TextField"/>
//         <div class="btn-group" role="group">
//             <button
//                 type="button"
//                 class="btn btn-primary btn-sm"
//                 t-on-click="fetchSuggestions"
//                 t-att-disabled="!props.value || this.state.cadastr == this.props.value">
//                 <i class="fa fa-hand-o-up me-1"></i>
//                 Получить адрес и координаты из НСПД
//             </button>
//         </div>
//         <ul t-if="state.suggestions.length">
//             <li class="fias-address-item" t-foreach="state.suggestions" t-as="suggestion" t-key="suggestion" t-on-click="selectSuggestion">
//                 <span class="fias-address-item__text" t-esc="suggestion" />
//             </li>
//         </ul>
//     `;

//   setup() {
//     super.setup();
//     this.state = useState({
//       suggestions: [],
//     });
//     // this.onInput = debounce(this.fetchSuggestions.bind(this), 300);
//     this.rpc = useService("rpc");
//     this.notification = useService("notification");
//   }

//   coordEPSG3857ToWGS84(coord) {
//     const x = coord[0];
//     const y = coord[1];
//     const R = 6378137; // Радиус Земли в метрах
//     const lon = (x / R) * (180 / Math.PI);
//     const lat =
//       (2 * Math.atan(Math.exp(y / R)) - Math.PI / 2) * (180 / Math.PI);
//     return [lat, lon];
//   }

//   async fetchSuggestions(ev) {
//     if (this.props.value) {
//       try {
//         this.state.cadastr = this.props.value;
//         const params = {
//           query: this.props.value,
//           // "Сооружения" 36328
//           // "Здания" 36049
//           layersId: 36049,
//           // "Земельные участки из ЕГРН" 36048
//           // layersId: 36048,
//         };
//         const urlParams = new URLSearchParams(params).toString();
//         const url = "https://nspd.gov.ru/api/geoportal/v2/search/geoportal?";
//         const response = await fetch(url + urlParams, {
//           headers: {
//             "User-Agent":
//               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
//             Referer: "https://nspd.gov.ru",
//             Host: "nspd.gov.ru",
//           },
//         });
//         if (response.ok) {
//           const data = await response.json();
//           console.log(data);
//           const address =
//             data["data"]["features"][0]["properties"]["options"][
//               "readable_address"
//             ];
//           // console.log(address);
//           // EPSG:3857
//           const coords = this.coordEPSG3857ToWGS84(
//             data["data"]["features"][0]["geometry"]["coordinates"][0][0]
//           );
//           // console.log(coords);
//           await this.props.record.update({
//             geo_address: address,
//             geo_latitude: coords[0],
//             geo_longitude: coords[1],
//           });
//         } else {
//           throw "Ошибка при получении адресов";
//         }
//       } catch (error) {
//         console.error("Ошибка при получении адреса НСПД:", error);
//         this.notification.add(
//           "Ошибка при получении адреса НСПД, попробуйте снова",
//           {
//             type: "danger",
//           }
//         );
//       }
//     } else {
//       this.state.suggestions = [];
//     }
//   }

//   selectSuggestion(event) {
//     this.props.update(event.target.innerText);
//     this.state.suggestions = [];
//   }
// }

// registry.category("fields").add("field_text_nspd", NspdTextField);
