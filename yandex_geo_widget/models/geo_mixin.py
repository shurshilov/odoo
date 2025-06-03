from odoo import models, fields, api


class GeoMixin(models.AbstractModel):
    """
    Mixin модель для добавления геокоординат к любой модели Odoo
    """

    _name = "geo.mixin"
    _description = "Геокоординаты Mixin"

    # Поля для хранения координат
    geo_latitude = fields.Float(
        string="Широта",
        digits=(10, 6),
        help="Географическая широта в десятичных градусах",
    )
    geo_longitude = fields.Float(
        string="Долгота",
        digits=(10, 6),
        help="Географическая долгота в десятичных градусах",
    )

    # Составное поле для отображения координат
    geo_coordinates = fields.Char(
        string="Координаты",
        compute="_compute_geo_coordinates",
        store=False,
        help='Географические координаты в формате "широта, долгота"',
    )

    # Поле для адреса (опционально)
    geo_address = fields.Text(
        string="Адрес", help="Адрес соответствующий геокоординатам"
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

    def set_geo_coordinates(self, latitude, longitude, address=None):
        """
        Устанавливает геокоординаты для записи

        :param latitude: широта
        :param longitude: долгота
        :param address: адрес (опционально)
        """
        self.ensure_one()
        vals = {
            "geo_latitude": latitude,
            "geo_longitude": longitude,
        }
        if address:
            vals["geo_address"] = address
        self.write(vals)

    def get_geo_coordinates(self):
        """
        Возвращает геокоординаты записи

        :return: словарь с координатами
        """
        self.ensure_one()
        return {
            "latitude": self.geo_latitude or 0,
            "longitude": self.geo_longitude or 0,
            "address": self.geo_address or "",
        }

    @api.model
    def get_default_map_center(self):
        """
        Возвращает центр карты по умолчанию
        Можно переопределить в наследующих моделях
        """
        # Координаты Ташкента по умолчанию
        return {"latitude": 41.2995, "longitude": 69.2401, "zoom": 10}
