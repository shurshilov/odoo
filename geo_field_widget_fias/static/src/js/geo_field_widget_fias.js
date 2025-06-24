/** @odoo-module **/

import { registry } from "@web/core/registry";
import { debounce } from "@web/core/utils/timing";
import { CharField, charField } from "@web/views/fields/char/char_field";
import { TextField, textField } from "@web/views/fields/text/text_field";
import { useService } from "@web/core/utils/hooks";
import { onWillStart, onMounted, useState, xml } from "@odoo/owl";

class FieldCharFias extends CharField {
  static template = xml`
        <t t-call="web.CharField"/>
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
    });
    this.rpc = useService("rpc");
    this.notification = useService("notification");
    onWillStart(this.willStart);
    onMounted(this.onMounted);
  }

  // вместо this.onInput в чар поле
  async inputListener(ev) {
    if (ev.target === this.input.el) {
      const debounce_fetch = debounce(this.fetchSuggestions.bind(this), 800);
      await debounce_fetch(ev);
    }
  }
  onMounted() {
    this.input.el.addEventListener("input", this.inputListener.bind(this));
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
    if (ev.target.value && window.fias_api_key) {
      try {
        const url = `https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressHint?search_string=${ev.target.value}&address_type=2`;
        const response = await fetch(url, {
          headers: { "master-token": window.fias_api_key },
        });
        if (response.ok) {
          const data = await response.json();
          this.state.suggestions = data["hints"].map(
            (item) => item["full_name"],
          );
        } else {
          console.error("Ошибка при получении адресов...");
        }
      } catch (error) {
        console.error("Ошибка при получении адресов:", error);
        this.notification.add(
          "Ошибка при получении адресов ФИАС, попробуйте снова",
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
    this.props.record.update({
      [this.props.name]: event.target.innerText,
    });
    this.state.suggestions = [];
  }
}

export const fiasCharField = {
  ...charField,
  component: FieldCharFias,
};
registry.category("fields").add("field_char_fias", fiasCharField);

class FiasTextField extends TextField {
  static template = xml`
        <t t-call="web.TextField"/>
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
    });
    // this.onInput = debounce(this.fetchSuggestions.bind(this), 800);
    this.rpc = useService("rpc");
    this.notification = useService("notification");
    onWillStart(this.willStart);
    onMounted(this.onMounted);
  }

  // вместо this.onInput в чар поле
  async inputListener(ev) {
    if (ev.target === this.textareaRef.el) {
      const debounce_fetch = debounce(this.fetchSuggestions.bind(this), 800);
      await debounce_fetch(ev);
    }
  }

  onMounted() {
    this.textareaRef.el.addEventListener(
      "input",
      this.inputListener.bind(this),
    );
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
    // запрос подсказок из сервиса ФИАС
    if (ev.target.value && window.fias_api_key) {
      try {
        const url = `https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressHint?search_string=${ev.target.value}&address_type=2`;
        const response = await fetch(url, {
          headers: {
            "master-token": window.fias_api_key,
            "User-Agent":
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
            Referer: "https://fias-public-service.nalog.ru",
            Host: "fias-public-service.nalog.ru",
          },
        });
        if (response.ok) {
          const data = await response.json();
          this.state.suggestions = data["hints"].map(
            (item) => item["full_name"],
          );
        } else {
          console.error("Ошибка при получении адресов...");
          this.state.suggestions = [];
        }
      } catch (error) {
        console.error("Ошибка при получении адресов:", error);
        this.state.suggestions = [];
        this.notification.add(
          "Ошибка при получении адресов ФИАС, попробуйте снова",
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
    this.props.record.update({
      [this.props.name]: event.target.innerText,
    });
    this.state.suggestions = [];
  }
}

export const fiasTextField = {
  ...textField,
  component: FiasTextField,
};
registry.category("fields").add("field_text_fias", fiasTextField);
