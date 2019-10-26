# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class pos_order(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _prepare_filter_for_pos(self, pos_session_id):
        return [
            ('state', 'in', ['paid', 'done', 'invoiced']),
        ]

    @api.model
    def _prepare_filter_query_for_pos(self, pos_session_id, query):
        return [
            '|',
            ('partner_id.name', 'ilike', query),
            ('partner_id.phone', 'ilike', query),
        ]

    @api.model
    def _prepare_fields_for_pos_list(self):
        return [
            'name', 'pos_reference', 'partner_id', 'date_order',
            'amount_total', 'amount_paid', 'session_id',
            'amount_tax', 'statement_ids', 'lines', 'invoice_id',
            'fiscal_position_id'
        ]

    @api.model
    def search_done_orders_for_pos(self, query, pos_session_id):
        session_obj = self.env['pos.session']
        config = session_obj.browse(pos_session_id).config_id
        condition = self._prepare_filter_for_pos(pos_session_id)
        if not query:
            # Search only this POS orders
            condition += [('config_id', '=', config.id),('date_order','>=',datetime.now().strftime('%Y-%m-%d'))]
        else:
            # Search globally by criteria
            condition += [('config_id', '=', config.id)] + self._prepare_filter_query_for_pos(pos_session_id, query)
        fields = self._prepare_fields_for_pos_list()
        receipt_ids = self.search_read(condition, fields, limit=config.iface_load_done_order_max_qty)
        return receipt_ids

    @api.multi
    def _prepare_done_order_for_pos(self):
        self.ensure_one()
        order_lines = []
        payment_lines = []
        for order_line in self.lines:
            order_line = self._prepare_done_order_line_for_pos(order_line)
            order_lines.append(order_line)
        for payment_line in self.statement_ids:
            payment_line = self._prepare_done_order_payment_for_pos(payment_line)
            payment_lines.append(payment_line)
        return {
            'id': self.id,
            'date_order': self.date_order,
            'pos_reference': self.pos_reference,
            'name': self.name,
            'partner_id': self.partner_id.id,
            'fiscal_position': self.fiscal_position_id.id,
            'line_ids': order_lines,
            'statement_ids': payment_lines,
        }

    @api.multi
    def _prepare_done_order_line_for_pos(self, order_line):
        self.ensure_one()
        return {
            'product_name': order_line.product_id.name,
            'product_id': order_line.product_id.id,
            'qty': order_line.qty,
            'price_unit': order_line.price_unit,
            'discount': order_line.discount,
        }

    @api.multi
    def _prepare_done_order_payment_for_pos(self, payment_line):
        self.ensure_one()
        return {
            'journal_id': payment_line.journal_id.id,
            'amount': payment_line.amount,
        }

    @api.multi
    def load_done_order_for_pos(self):
        self.ensure_one()
        return self._prepare_done_order_for_pos()