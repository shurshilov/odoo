from odoo import api, fields, models


class GeoMixin(models.AbstractModel):
    """
    Mixin модель для добавления геокоординат к любой модели Odoo
    """

    _name = "geo.mixin"
    _description = "Геокоординаты Mixin"

    # Поля для хранения координат
    geo_latitude = fields.Float(
        string="Широта",
        digits=(15, 12),
        help="Географическая широта в десятичных градусах",
    )
    geo_longitude = fields.Float(
        string="Долгота",
        digits=(15, 12),
        help="Географическая долгота в десятичных градусах",
    )

    # Составное поле для отображения координат
    geo_coordinates = fields.Char(
        string="Координаты",
        compute="_compute_geo_coordinates",
        store=False,
        help='Географические координаты в формате "широта, долгота"',
    )

    # geo_coordinates_last_updated = fields.Datetime(
    #     string="Координаты последний раз обновлено",
    # )

    # Поле для адреса (опционально)
    geo_address = fields.Text(
        string="Адрес", help="Адрес соответствующий геокоординатам"
    )

    # geo_address_last_updated = fields.Datetime(
    #     string="Адрес последний раз обновлено",
    # )

    geo_cadastr = fields.Char(
        string="Кадастровый номер",
        help="Пример 77:05:0006004:117",
    )

    @api.depends("geo_latitude", "geo_longitude")
    def _compute_geo_coordinates(self):
        """Вычисляет строковое представление координат"""
        for record in self:
            if record.geo_latitude and record.geo_longitude:
                record.geo_coordinates = (
                    f"{record.geo_latitude:.6f}, {record.geo_longitude:.6f}"
                )
            else:
                record.geo_coordinates = ""

    # def set_geo_coordinates(self, latitude, longitude, address=None):
    #     """
    #     Устанавливает геокоординаты для записи

    #     :param latitude: широта
    #     :param longitude: долгота
    #     :param address: адрес (опционально)
    #     """
    #     self.ensure_one()
    #     vals = {
    #         "geo_latitude": latitude,
    #         "geo_longitude": longitude,
    #     }
    #     if address:
    #         vals["geo_address"] = address
    #     self.write(vals)

    # def get_geo_coordinates(self):
    #     """
    #     Возвращает геокоординаты записи

    #     :return: словарь с координатами
    #     """
    #     self.ensure_one()
    #     return {
    #         "latitude": self.geo_latitude or 0,
    #         "longitude": self.geo_longitude or 0,
    #         "address": self.geo_address or "",
    #     }

    # @api.model
    # def get_default_map_center(self):
    #     """
    #     Возвращает центр карты по умолчанию
    #     Можно переопределить в наследующих моделях
    #     """
    #     # Координаты Москвы по умолчанию
    #     return {"latitude": 55.75222, "longitude": 37.61556, "zoom": 10}

    # def search_addresses(self, query, limit=10):
    #     """Поиск адресов через Yandex Geocoder API"""
    #     api_key = self.get_yandex_api_key()
    #     if not api_key:
    #         return []

    #     try:
    #         import requests

    #         url = "https://geocode-maps.yandex.ru/1.x/"
    #         params = {
    #             "apikey": api_key,
    #             "geocode": query,
    #             "format": "json",
    #             "results": limit,
    #             "lang": "ru_RU",
    #         }

    #         response = requests.get(url, params=params, timeout=10)
    #         response.raise_for_status()

    #         data = response.json()
    #         suggestions = []

    #         if "response" in data and "GeoObjectCollection" in data["response"]:
    #             geo_objects = data["response"]["GeoObjectCollection"]["featureMember"]

    #             for obj in geo_objects:
    #                 geo_object = obj["GeoObject"]
    #                 point = geo_object["Point"]["pos"].split()

    #                 suggestion = {
    #                     "text": geo_object["metaDataProperty"]["GeocoderMetaData"][
    #                         "text"
    #                     ],
    #                     "longitude": float(point[0]),
    #                     "latitude": float(point[1]),
    #                     "data": geo_object,
    #                 }
    #                 suggestions.append(suggestion)

    #         return suggestions

    #     except Exception as e:
    #         _logger.error(f"Ошибка при поиске адресов Yandex: {e}")
    #         return []

    # @api.model
    # def yandex_search_addresses(self, query):
    #     """API метод для поиска адресов (вызывается из JS)"""
    #     return self.search_addresses(query)
