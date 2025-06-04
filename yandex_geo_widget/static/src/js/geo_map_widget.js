/** @odoo-module **/

import { registry } from "@web/core/registry";
import { onMounted, onWillUnmount, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { FloatField } from "@web/views/fields/float/float_field";

export class YandexMapsWidget extends FloatField {
  setup() {
    super.setup();
    this.rpc = useService("rpc");
    this.notification = useService("notification");
    this.mapRef = useRef("mapContainer");

    this.state = useState({
      isMapLoaded: false,
      isApiLoaded: false,
      currentLat: this.props.record.data.geo_latitude || 55.75222,
      currentLng: this.props.record.data.geo_longitude || 37.61556,
      currentAddress: this.props.record.data.geo_address,
    });

    this.map = null;
    this.placemark = null;
    this.api_key = "";

    onMounted(() => {
      this.loadYandexMapsAPI();
    });

    onWillUnmount(() => {
      if (this.map) {
        this.map.destroy();
      }
    });
  }

  async loadYandexMapsAPI() {
    if (window.ymaps) {
      this.initializeMap();
      return;
    }

    try {
      this.api_key = await this.rpc("/web/dataset/call_kw", {
        model: "geo.mixin",
        method: "get_yandex_api_key",
        kwargs: {},
        args: [],
      });
      // console.log("this.api_key", this.api_key);
      // Загружаем API Yandex Maps
      const script = document.createElement("script");
      script.type = "text/javascript";
      script.src = `https://api-maps.yandex.ru/2.1/?apikey=${this.api_key}&lang=ru_RU`;
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
            6,
          )}, ${this.state.currentLng.toFixed(6)}`,
        },
        {
          preset: "islands#redDotIcon",
          draggable: true,
        },
      );

      // Обработчик перетаскивания метки
      this.placemark.events.add("dragend", (e) => {
        const coords = e.get("target").geometry.getCoordinates();
        this.state.currentLat = coords[0];
        this.state.currentLng = coords[1];
        this.updatePlacemarkBalloon();
      });

      // Обработчик клика по карте
      this.map.events.add("click", (e) => {
        const coords = e.get("coords");
        this.state.currentLat = coords[0];
        this.state.currentLng = coords[1];
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
        )}, ${this.state.currentLng.toFixed(6)}`,
      );
    }
  }

  get geo_coords_changed() {
    return (
      this.state.currentLat != this.props.record.data.geo_latitude ||
      this.state.currentLng != this.props.record.data.geo_longitude
    );
  }

  get geo_address_changed() {
    return this.state.currentAddress != this.props.record.data.geo_address;
  }

  async saveCoordinates() {
    try {
      const values = {
        geo_latitude: this.state.currentLat,
        geo_longitude: this.state.currentLng,
      };

      if (!this.api_key)
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
          if (address) {
            values["geo_address"] = address;
            this.state.currentAddress = address;
          } else {
            values["geo_address"] = "";
          }
        } else {
          values["geo_address"] = "";
        }
        // }
      }
      values["_sync"] = !this.geo_coords_changed && !this.geo_address_changed;
      await this.props.record.update(values);
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
    if (!this.api_key)
      this.notification.add(
        "У вас не установлен api key Yandex Maps API, работа с адресом не доступна",
        {
          type: "danger",
        },
      );
    else {
      // if (this.geo_address_changed) {
      const response = await window.ymaps.geocode(
        this.props.record.data.geo_address,
        {
          results: 1,
        },
      );

      const firstGeoObject = response.geoObjects.get(0);
      if (firstGeoObject) {
        const coords = firstGeoObject.geometry.getCoordinates();
        this.state.currentLat = coords[0];
        this.state.currentLng = coords[1];
        this.state.currentAddress = this.props.record.data.geo_address;
        const values = {
          geo_latitude: this.state.currentLat,
          geo_longitude: this.state.currentLng,
        };
        values["_sync"] = !this.geo_coords_changed && !this.geo_address_changed;
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
    if (!this.api_key) {
      this.notification.add(
        "У вас не установлен api key Yandex Maps API, работа с адресом не доступна",
        {
          type: "danger",
        },
      );
    } else {
      // if (this.geo_address_changed) {
      const response = await window.ymaps.geocode(
        [
          this.props.record.data.geo_latitude,
          this.props.record.data.geo_longitude,
        ],
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
        values["_sync"] = !this.geo_coords_changed && !this.geo_address_changed;
        await this.props.record.update({
          geo_address: this.state.currentAddress,
        });
      }
    }

    this.state.currentLat = this.props.record.data.geo_latitude;
    this.state.currentLng = this.props.record.data.geo_longitude;
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

  // _onAddressInput(e) {
  //   var self = this;
  //   var query = e.target.value;

  //   clearTimeout(this.searchTimeout);

  //   if (query.length < 3) {
  //     this.$(".o_yandex_suggestions").empty();
  //     return;
  //   }

  //   this.searchTimeout = setTimeout(function () {
  //     self._searchAddresses(query);
  //   }, 300);
  // }

  // _searchAddresses(query) {
  //   var self = this;

  //   this._rpc({
  //     model: this.model,
  //     method: "yandex_search_addresses",
  //     args: [query],
  //   }).then(function (suggestions) {
  //     self._renderSuggestions(suggestions);
  //   });
  // }
}

YandexMapsWidget.template = "yandex_maps_widget.YandexMapsWidget";
// YandexMapsWidget.props = {
//   ...Component.props,
//   record: Object,
//   height: { type: String, optional: true },
// };

registry.category("fields").add("geo_yandex_map", YandexMapsWidget);
