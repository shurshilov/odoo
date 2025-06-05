from odoo import models, api


class YandexSettings(models.AbstractModel):
    """
    Yandex settings model
    """

    _name = "yandex.settings"
    _description = "Yandex settings model"

    @api.model
    def get_api_key(self):
        """Получение API ключа Yandex из системных параметров"""
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("geo_field_widget_yandex.api_key", "")
        )
