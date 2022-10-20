from odoo import api
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _search_build_domain(self, domain_list, search, fields, extra=None):
        """
        Builds a search domain AND-combining a base domain with partial matches of each term in
        the search expression in any of the fields.

        :param domain_list: base domain list combined in the search expression
        :param search: search expression string
        :param fields: list of field names to match the terms of the search expression with
        :param extra: function that returns an additional subdomain for a search term

        :return: domain limited to the matches of the search expression
        """
        fields.append("tag_ids")
        return super()._search_build_domain(domain_list, search, fields, extra=None)
