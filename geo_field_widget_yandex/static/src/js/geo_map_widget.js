/** @odoo-module **/

import { registry } from "@web/core/registry";
import { onMounted, onWillUnmount, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { FloatField, floatField } from "@web/views/fields/float/float_field";

export class YandexMapsWidget extends FloatField {
  static template = "yandex_maps_widget.YandexMapsWidget";
  static props = {
    ...FloatField.props,
    fieldNameLat: { type: String, optional: true },
    fieldNameLng: { type: String, optional: true },
    fieldNameAddress: { type: String, optional: true },
    height: { type: String, optional: true },
  };

  setup() {
    super.setup();
    this.rpc = useService("rpc");
    this.notification = useService("notification");
    this.mapRef = useRef("mapContainer");

    this.state = useState({
      isMapLoaded: false,
      isApiLoaded: false,
      currentLat: this.latitude,
      currentLng: this.longitude,
      currentAddress: this.address,
    });

    this.map = null;
    this.placemark = null;
    // this.api_key = "";

    onMounted(() => {
      this.loadYandexMapsAPI();
    });

    onWillUnmount(() => {
      if (this.map) {
        this.map.destroy();
      }
    });
  }

  get latitude() {
    return this.props.record.data[this.props.fieldNameLat] || 55.75222;
  }

  get longitude() {
    return this.props.record.data[this.props.fieldNameLng] || 37.61556;
  }

  get address() {
    return this.props.record.data[this.props.fieldNameAddress] || "";
  }

  get geo_coords_changed() {
    return (
      this.state.currentLat != this.latitude ||
      this.state.currentLng != this.longitude
    );
  }

  get geo_address_changed() {
    return this.state.currentAddress != this.address;
  }

  async loadYandexMapsAPI() {
    if (window.ymaps) {
      this.initializeMap();
      return;
    }

    try {
      window.yandex_api_key = await this.rpc("/web/dataset/call_kw", {
        model: "yandex.settings",
        method: "get_api_key",
        kwargs: {},
        args: [],
      });
      // Загружаем API Yandex Maps
      const script = document.createElement("script");
      script.type = "text/javascript";
      script.src = `https://api-maps.yandex.ru/2.1/?apikey=${window.yandex_api_key}&lang=ru_RU`;
      script.onload = () => {
        window.ymaps.ready(() => {
          this.state.isApiLoaded = true;
          this.initializeMap();
        });
      };
      script.onerror = () => {
        this.notification.add("Ошибка загрузки Yandex Maps API", {
          type: "danger",
        });
      };
      document.head.appendChild(script);
    } catch (error) {
      console.error("Ошибка загрузки Yandex Maps:", error);
      this.notification.add("Ошибка загрузки карты", {
        type: "danger",
      });
    }
  }

  initializeMap() {
    if (!window.ymaps || !this.mapRef.el) return;

    try {
      // Создаем карту
      this.map = new window.ymaps.Map(this.mapRef.el, {
        center: [this.state.currentLat, this.state.currentLng],
        zoom: 12,
        controls: ["zoomControl", "typeSelector", "fullscreenControl"],
      });

      // Создаем метку
      this.placemark = new window.ymaps.Placemark(
        [this.state.currentLat, this.state.currentLng],
        {
          hintContent: "Перетащите метку для изменения координат",
          balloonContent: `Координаты: ${this.state.currentLat.toFixed(
            12,
          )}, ${this.state.currentLng.toFixed(12)}`,
        },
        {
          preset: "islands#redDotIcon",
          draggable: true,
        },
      );

      // Обработчик перетаскивания метки
      this.placemark.events.add("dragend", (e) => {
        const coords = e.get("target").geometry.getCoordinates();
        this.state.currentLat = parseFloat(coords[0].toFixed(12));
        this.state.currentLng = parseFloat(coords[1].toFixed(12));
        this.state.currentAddress = "";
        this.updatePlacemarkBalloon();
      });

      // Обработчик клика по карте
      this.map.events.add("click", (e) => {
        const coords = e.get("coords");
        this.state.currentLat = parseFloat(coords[0].toFixed(12));
        this.state.currentLng = parseFloat(coords[1].toFixed(12));
        this.state.currentAddress = "";
        this.placemark.geometry.setCoordinates(coords);
        this.updatePlacemarkBalloon();
      });

      this.map.geoObjects.add(this.placemark);
      this.state.isMapLoaded = true;
    } catch (error) {
      console.error("Ошибка инициализации карты:", error);
      this.notification.add("Ошибка инициализации карты", {
        type: "danger",
      });
    }
  }

  updatePlacemarkBalloon() {
    if (this.placemark) {
      this.placemark.properties.set(
        "balloonContent",
        `Координаты: ${this.state.currentLat.toFixed(
          6,
        )}, ${this.state.currentLng.toFixed(12)}`,
      );
    }
  }

  async saveCoordinates() {
    try {
      const values = {
        geo_latitude: this.state.currentLat,
        geo_longitude: this.state.currentLng,
        geo_address: "",
      };

      if (!window.yandex_api_key)
        this.notification.add(
          "У вас не установлен api key Yandex Maps API, работа с адресом не доступна",
          {
            type: "warning",
          },
        );
      else {
        // if (this.geo_coord_changed) {
        const response = await window.ymaps.geocode(
          [this.state.currentLat, this.state.currentLng],
          {
            results: 1,
          },
        );

        const firstGeoObject = response.geoObjects.get(0);
        if (firstGeoObject) {
          const address = firstGeoObject.getAddressLine();
          if (address) values["geo_address"] = address;
        }
        // }
      }

      await this.props.record.update(values);
      this.state.currentAddress = values["geo_address"];
      this.state.currentLat = values["geo_latitude"];
      this.state.currentLng = values["geo_longitude"];
      console.log(values);
      // await this.props.record.save();
      // this.notification.add("Координаты успешно сохранены", {
      //   type: "success",
      // });
    } catch (error) {
      console.error("Ошибка сохранения координат:", error);
      this.notification.add("Ошибка сохранения координат", {
        type: "danger",
      });
    }
  }

  async setAddressLocation() {
    if (!window.yandex_api_key)
      this.notification.add(
        "У вас не установлен api key Yandex Maps API, работа с адресом не доступна",
        {
          type: "danger",
        },
      );
    else {
      // if (this.geo_address_changed) {
      const response = await window.ymaps.geocode(this.address, {
        results: 1,
      });

      const firstGeoObject = response.geoObjects.get(0);
      if (firstGeoObject) {
        const coords = firstGeoObject.geometry.getCoordinates();
        console.log(coords);
        this.state.currentLat = parseFloat(coords[0].toFixed(12));
        this.state.currentLng = parseFloat(coords[1].toFixed(12));
        this.state.currentAddress = this.address;
        const values = {
          geo_latitude: this.state.currentLat,
          geo_longitude: this.state.currentLng,
        };
        await this.props.record.update(values);
        this.resetToCurrentLocation();
      }
      // } else {
      //   this.notification.add("Адрес не изменился, задайте другой адрес", {
      //     type: "warning",
      //   });
      // }
    }
  }

  resetToCurrentLocation() {
    const lat = this.state.currentLat;
    const lng = this.state.currentLng;

    if (this.map && this.placemark) {
      this.map.setCenter([lat, lng], 15);
      this.placemark.geometry.setCoordinates([lat, lng]);
      this.updatePlacemarkBalloon();
    }
  }

  async resetToSavedLocation() {
    if (!window.yandex_api_key) {
      this.notification.add(
        "У вас не установлен api key Yandex Maps API, работа с адресом не доступна",
        {
          type: "danger",
        },
      );
    } else {
      // if (this.geo_address_changed) {
      const response = await window.ymaps.geocode(
        [this.latitude, this.longitude],
        {
          results: 1,
        },
      );
      const firstGeoObject = response.geoObjects.get(0);
      if (firstGeoObject) {
        const address = firstGeoObject.getAddressLine();
        if (address) {
          this.state.currentAddress = address;
        } else {
          this.state.currentAddress = "";
        }
        await this.props.record.update({
          geo_address: this.state.currentAddress,
        });
      }
    }

    this.state.currentLat = this.latitude;
    this.state.currentLng = this.longitude;
    this.resetToCurrentLocation();
  }

  resetToMyLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;

          this.state.currentLat = lat;
          this.state.currentLng = lng;

          if (this.map && this.placemark) {
            this.map.setCenter([lat, lng], 15);
            this.placemark.geometry.setCoordinates([lat, lng]);
            this.updatePlacemarkBalloon();
          }
        },
        (error) => {
          console.error("Ошибка получения геолокации:", error);
          this.notification.add("Не удалось получить текущее местоположение", {
            type: "warning",
          });
        },
      );
    } else {
      this.notification.add("Геолокация не поддерживается браузером", {
        type: "warning",
      });
    }
  }

  get mapHeight() {
    return this.props.height || "400px";
  }
}

export const yandexMapsWidget = {
  ...floatField,
  component: YandexMapsWidget,
  extractProps({ options }) {
    // добавить возможность установить любое поле
    const props = floatField.extractProps(...arguments);
    props.fieldNameLat = options.field_name_lat || "geo_latitude";
    props.fieldNameLng = options.field_name_lng || "geo_longitude";
    props.fieldNameAddress = options.field_name_address || "geo_address";
    return props;
  },
};

registry.category("fields").add("field_float_yandex_map", yandexMapsWidget);
