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
    });

    this.map = null;
    this.placemark = null;

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
      // Загружаем API Yandex Maps
      const script = document.createElement("script");
      script.src = "https://api-maps.yandex.ru/2.1/?apikey=&lang=ru_RU";
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
        zoom: 10,
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

  async saveCoordinates() {
    try {
      const values = {
        geo_latitude: this.state.currentLat,
        geo_longitude: this.state.currentLng,
      };

      await this.props.record.update(values);

      this.notification.add("Координаты успешно сохранены", {
        type: "success",
      });
    } catch (error) {
      console.error("Ошибка сохранения координат:", error);
      this.notification.add("Ошибка сохранения координат", {
        type: "danger",
      });
    }
  }

  resetToSavedLocation() {
    const lat = this.props.record.data.geo_latitude;
    const lng = this.props.record.data.geo_longitude;

    if (this.map && this.placemark) {
      this.map.setCenter([lat, lng], 15);
      this.placemark.geometry.setCoordinates([lat, lng]);
      this.updatePlacemarkBalloon();
    }
  }
  resetToCurrentLocation() {
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

YandexMapsWidget.template = "yandex_maps_widget.YandexMapsWidget";
// YandexMapsWidget.props = {
//   ...Component.props,
//   record: Object,
//   height: { type: String, optional: true },
// };

registry.category("fields").add("geo_yandex_map", YandexMapsWidget);
