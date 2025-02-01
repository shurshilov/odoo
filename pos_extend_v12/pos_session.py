# copyright Spellbound Soft Solutions
from odoo import api, fields, models, _

# from numpy.core.defchararray import count


class PosSession(models.Model):
    _inherit = "pos.session"

    def seetion_total(self):
        for rec in self:
            order_id = self.env["pos.order"].search([("session_id", "=", rec.name)])
            if order_id:
                # print "order is.......................................",order_id
                rec.number_of_order = len(order_id)
                cancel = 0
                done = 0
                for order in order_id:
                    for each in order.lines:
                        rec.subtotal_session += each.price_subtotal_incl
                        rec.untaxamount_total += each.price_subtotal
                        if each.discount:
                            rec.total_discount += (each.price_unit * each.qty) - each.price_subtotal
                        rec.sale_qty += each.qty
                    rec.tax_amount += order.amount_tax
                    if order.state == "cancel":
                        cancel += 1
                    if order.state == "done" or order.state == "invoiced":
                        done += 1
                rec.total_cancel_order = cancel
                rec.total_done_order = done
                if order.session_id.state == "closed":
                    rec.number_of_order = 0
                    rec.total_discount = 0.0
                    rec.sale_qty = 0
                    rec.total_done_order = 0
                    rec.total_cancel_order = 0
                    rec.subtotal_session = 0
                    rec.untaxamount_total = 0
                    rec.tax_amount = 0

    untaxamount_total = fields.Float("Total", compute="seetion_total", digits=(16, 2))
    tax_amount = fields.Float("Total VAT", compute="seetion_total", digits=(16, 2))
    subtotal_session = fields.Float("Subtotal", compute="seetion_total", digits=(16, 2))
    number_of_order = fields.Integer("Total Order", compute="seetion_total")
    total_discount = fields.Float("Total discount", compute="seetion_total")
    sale_qty = fields.Integer("Total Qty Sale", compute="seetion_total")
    total_done_order = fields.Integer("Total Done Order", compute="seetion_total")
    total_cancel_order = fields.Integer("Total Cancel Order", compute="seetion_total")


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    price_subtotal = fields.Float(
        compute="_compute_amount_line_all", digits=0, string="Subtotal w/o Tax", store=True
    )
    price_subtotal_incl = fields.Float(
        compute="_compute_amount_line_all", digits=0, string="Subtotal", store=True
    )


class PosConfig(models.Model):
    _inherit = "pos.config"

    def session_payment(self):
        for res in self:
            details = []
            bg_colore = [
                "",
                "cadetblue",
                "rosybrown",
                "rosyblue",
                "coral",
                "darkcyan",
                "lightcoral",
                "cornflowerblue",
                "cadetblue",
                "rosybrown",
                "rosyblue",
                "coral",
                "darkcyan",
                "lightcoral",
                "cornflowerblue",
            ]
            total = 0
            for session in res.session_ids:
                payment_id = self.env["account.bank.statement"].search(
                    [("name", "=", session.name)]
                )
                for each in payment_id:
                    session_id = self.env["pos.session"].search([("name", "=", each.name)])
                    if session_id.state == "opened":
                        # print "%%%%%%%%%%%%%%%%%%%%%%%",each.currency_id.name
                        # print "Journal namee get",each.journal_id.name_get()[0][1]
                        details.append(
                            {
                                "payment": each.journal_id.name_get()[0][1],
                                "amount": each.total_entry_encoding,
                                "currency": each.currency_id.symbol,
                            }
                        )
                        total += each.total_entry_encoding
                # print "\n details-000000000----", details
            body = """<table  style='width: 100%;'>"""
            count = 0
            for data in details:
                # print "#######################",data['currency']
                count += 1
                size = (data["amount"] * 100) / total if data["amount"] else 0
                body += """<tr>"""
                body += (
                    """<td style="text-align:left;width: 40%;/* font-size: 16px; */color: blue;">"""
                    + data["payment"]
                    + """</td>"""
                )
                body += (
                    """<td style="text-align:left; width: 70%;">
               <div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"
                    style="width:"""
                    + "100"
                    + """%;background-color:white;border-radius:10px;height:16px; -moz-border-radius: 3px;-webkit-border-radius:
                                10px;border:1px solid #f0eeef;">
                    <div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"
                    style="width:"""
                    + format(size, ".0f")
                    + """%;background-color:"""
                    + bg_colore[count]
                    + """;height:14px;border-radius:10px; -moz-border-radius: 3px;-webkit-border-radius:
                                10px;line-height: 14px;font-size: 10px;color:black;">"""
                    + format(size, ".0f")
                    + "%"
                    + """
                                </div>
                </div>
                </td>
               """
                )
                body += (
                    """<td style="text-align:left;color:  firebrick;width: 20%;"><div style='margin-left: 5px;'>"""
                    + data["currency"]
                    + str(data["amount"])
                    + """</div></td>"""
                )
                body += """</tr>"""
            body += "</table>"
            res.payment_details = body

    def session_total_count(self):
        session_list = self.env["pos.session"].search([("state", "=", "opened")])

        for sessions in session_list:
            # config_ids = self.env['pos.config'].search[('id','in',sessions.config_id)]

            for each1 in sessions.config_id:
                each1.total_sesstion = len(sessions)

                each1.total_details_count = (
                    """

                                <table style="height: 24px;" width="100%">
                                <tbody>
                                    <tr>
                                        <td style="width: 55%;">Subtotal w/o Tax:</td>
                                        <td style="width: 40%;">
                                            <div class="progress mb0" style="height: 15px;width:100%" >

                                                    <div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"
                                                        style="width:"""
                    + format(
                        (each1.untaxamount_total * 100) / each1.subtotal_session
                        if each1.untaxamount_total
                        else 0,
                        ".0f",
                    )
                    + """%;background-color:rosybrown;">
                                                        <span style="font-size:0px;display:  initial;">"""
                    + str(each1.untaxamount_total)
                    + """</span>

                                                    </div>
                                            </div>
                                        </td>
                                        <td style="width: 5%;margin-bottom: 3px;">"""
                    + str(round(each1.untaxamount_total, 2))
                    + """</td>
                                    </tr>
                                    <tr>
                                        <td style="width: 55%;margin-top: 10px;">Total Tax:</td>
                                        <td style="width: 40%;margin-top: 10px;">
                                            <div class="progress mb0" style="height: 15px;width:100%" >

                                                    <div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"
                                                        style="width:"""
                    + format(
                        (each1.tax_amount * 100) / each1.subtotal_session
                        if each1.tax_amount
                        else 0,
                        ".0f",
                    )
                    + """%;background-color:limegreen;">
                                                       <span style="font-size:0px;display:  initial;"> """
                    + str(each1.tax_amount)
                    + """</span>
                                                    </div>
                                            </div>
                                        </td>
                                        <td style="width: 5%;margin-bottom: 3px;">"""
                    + str(round(each1.tax_amount, 2))
                    + """</td>
                                    </tr>
                                    <tr>
                                        <td style="width: 55%;margin-top: 10px;">Subtotal:</td>
                                        <td style="width: 40%;margin-top: 10px;">
                                            <div class="progress mb0" style="height: 15px;width:100%" >
                                                    <div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"
                                                        style="width: """
                    + format(
                        (each1.subtotal_session * 100) / each1.subtotal_session
                        if each1.subtotal_session
                        else 0,
                        ".0f",
                    )
                    + """%;">
                                                         <span style="font-size:0px;display:  initial;"> """
                    + str(each1.subtotal_session)
                    + """</span>
                                                    </div>
                                            </div>
                                        </td>
                                         <td style="width: 5%;margin-bottom: 3px;">"""
                    + str(round(each1.subtotal_session, 2))
                    + """</td>
                                    </tr>
                                </tbody>
                            </table>

                        """
                )

    untaxamount_total = fields.Float(
        "Total", related="session_ids.untaxamount_total", digits=(16, 2)
    )
    tax_amount = fields.Float("Total VAT", related="session_ids.tax_amount", digits=(16, 2))
    subtotal_session = fields.Float(
        "Subtotal", related="session_ids.subtotal_session", digits=(16, 2)
    )
    number_of_order = fields.Integer("Total Order", related="session_ids.number_of_order")
    total_discount = fields.Float("Total discount(%)", related="session_ids.total_discount")
    sale_qty = fields.Integer("Total Qty Sale", related="session_ids.sale_qty")
    total_done_order = fields.Integer("Total Done Order", related="session_ids.total_done_order")
    total_cancel_order = fields.Integer(
        "Total Cancel Order", related="session_ids.total_cancel_order"
    )
    payment_details_ids = fields.One2many(
        "account.bank.statement",
        "pos_session_id",
        string="Payments",
        relared="session_ids.statement_ids",
        store=True,
        readonly=True,
    )
    payment_details = fields.Html("Payment Details", compute="session_payment")
    payment_graph = fields.Html("Payment Graph", compute="session_payment")

    total_details_count = fields.Html("Total Details", compute="session_total_count")
    total_sesstion = fields.Integer("Total", compute="session_total_count")

    @api.multi
    def get_action_pos_order(self):
        return {
            "name": _("Pos order"),
            "type": "ir.actions.act_window",
            "res_model": "pos.order",
            "view_mode": "tree",
            "view_type": "form",
            "domain": [("session_id", "=", self.session_ids.id)],
        }
