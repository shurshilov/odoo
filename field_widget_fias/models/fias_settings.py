from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class FiasSettings(models.AbstractModel):
    """
    Fias settings model
    """

    _name = "fias.settings"
    _description = "Fias settings model"

    @api.model
    def get_api_key(self):
        """Получение API ключа fias из системных параметров"""
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("field_widget_fias.api_key", "")
        )
