from odoo import api, fields, models
from odoo.addons.base.models.ir_mail_server import extract_rfc2822_addresses


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    user_ids = fields.One2many(
        comodel_name="res.users",
        compute="_compute_user_ids",
        string="Users",
        compute_sudo=True,
    )
    ir_mail_popular_id = fields.Many2one(
        "ir.mail_popular", string="Popular server settings"
    )

    @api.depends("smtp_user")
    def _compute_user_ids(self):
        for rec in self:
            rec.user_ids = self.env["res.users"].search(
                [("partner_id.email", "=", rec.smtp_user)]
            )

    @api.onchange("ir_mail_popular_id")
    def onchange_ir_mail_popular_id(self):
        for rec in self:
            rec.smtp_host = rec.ir_mail_popular_id.smtp_host
            rec.smtp_port = rec.ir_mail_popular_id.smtp_port
            rec.smtp_encryption = rec.ir_mail_popular_id.smtp_encryption
            rec.smtp_debug = rec.ir_mail_popular_id.smtp_debug

    @api.model
    def send_email(
        self,
        message,
        mail_server_id=None,
        smtp_server=None,
        smtp_port=None,
        smtp_user=None,
        smtp_password=None,
        smtp_encryption=None,
        smtp_debug=False,
        smtp_session=None,
    ):
        # Use the default bounce address **only if** no Return-Path was
        # provided by caller.  Caller may be using Variable Envelope Return
        # Path (VERP) to detect no-longer valid email addresses.
        smtp_from = (
            message["Return-Path"]
            or self._get_default_bounce_address()
            or message["From"]
        )
        assert (
            smtp_from
        ), "The Return-Path or From header is required for any outbound email"

        # The email's "Envelope From" (Return-Path), and all recipient addresses must only contain ASCII characters.
        from_rfc2822 = extract_rfc2822_addresses(smtp_from)
        assert from_rfc2822, (
            "Malformed 'Return-Path' or 'From' address: %r - "
            "It should contain one valid plain ASCII email"
        ) % smtp_from

        server_id = self.search([("smtp_user", "in", from_rfc2822)])

        if server_id:
            if "Return-Path" in message:
                message.replace_header("Return-Path", from_rfc2822[0])

        return super().send_email(
            message,
            mail_server_id,
            smtp_server,
            smtp_port,
            smtp_user,
            smtp_password,
            smtp_encryption,
            smtp_debug,
            smtp_session,
        )


class MailMail(models.Model):
    _inherit = "mail.mail"

    def send(self, auto_commit=False, raise_exception=False):
        for email in self.browse(self.ids):
            from_rfc2822 = extract_rfc2822_addresses(email.email_from)
            server_id = self.env["ir.mail_server"].search(
                [("smtp_user", "in", from_rfc2822)], limit=1
            )
            if server_id:
                self.write(
                    {
                        "mail_server_id": server_id.id,
                        "reply_to": email.email_from,
                    }
                )
            # else:
            #     server_id = self.env['ir.mail_server'].search([], order="sequence", limit=1)
            #     if server_id:
            #         self.write({'mail_server_id': server_id.id,'email_from': server_id.smtp_user,'reply_to': server_id.smtp_user})

            return super().send(
                auto_commit=auto_commit, raise_exception=raise_exception
            )
