# from odoo import models, fields, api
# import logging

# _logger = logging.getLogger(__name__)


# class NspdSettings(models.AbstractModel):
#     """
#     Nspd settings model
#     """

#     _name = "nspd.settings"
#     _description = "Nspd settings model"

#     @api.model
#     def get_api_key(self):
#         """Получение API ключа nspd из системных параметров"""
#         return (
#             self.env["ir.config_parameter"]
#             .sudo()
#             .get_param("field_widget_nspd.api_key", "")
#         )
# from pynspd import ThemeId
# from pynspd import Nspd, NspdFeature

# with Nspd() as nspd:
#     # Ваш код здесь...

#     # feat: NspdFeature | None = nspd.find(
#     #     "77:05:0001005:19", ThemeId.REAL_ESTATE_OBJECTS
#     # )
#     # NspdFeature.by_title("")
#     feat = nspd.find_in_layer(
#         "77:06:0002007:1014", NspdFeature.by_title("Земельные участки из ЕГРН")
#     )
# {
#     "title": "Земельные участки из ЕГРН",
#     "layerTreeId": 72,
#     "layerId": 36048,
#     "layerType": "wms",
#     "geometryType": "POLYGON",
#     "layerName": "Росреестр: Земельные участки ЕГРН",
#     "layerVisibleByDefault": False,
#     "categoryId": 36368,
# }
