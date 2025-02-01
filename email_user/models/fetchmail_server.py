import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class FetchmailServer(models.Model):
    _inherit = "fetchmail.server"

    per_user = fields.Boolean(
        "Enable per user mode",
        help="If disabled, work as usually in odoo. If enable, work directly from user email",
        default=True,
    )
    per_user_only_new = fields.Boolean(
        "Start from last uid",
        help="If enable, will fetch only new email after test connection",
        default=True,
    )
    per_user_auto_generate_channel = fields.Boolean(
        "Auto generate channel",
        help="If enable, will create channel with alias for catch non reply messages",
        default=True,
    )
    last_uid = fields.Integer(string="Last message UID", default=1)

    ir_mail_popular_id = fields.Many2one(
        "ir.mail_popular", string="Popular server settings"
    )

    @api.onchange("ir_mail_popular_id")
    def onchange_ir_mail_popular_id(self):
        for rec in self:
            rec.server = rec.ir_mail_popular_id.imap_host
            rec.port = rec.ir_mail_popular_id.imap_port
            rec.is_ssl = rec.ir_mail_popular_id.imap_encryption
            rec.server_type = "imap"

    # @api.constrains('per_user', 'server_type')
    # def _check_pec(self):
    #     for record in self:
    #         if record.per_user and record.server_type != 'imap':
    #             raise ValidationError(_("Email per user mail server must be of type IMAP."))

    def button_confirm_login(self):
        super().button_confirm_login()
        for server in self:
            if server.per_user and server.per_user_only_new:
                server.button_get_last_uid()
            if server.per_user and server.per_user_auto_generate_channel:
                server.button_create_channel_no_reply_messages()

    def button_create_channel_no_reply_messages(self):
        """Auto generate channel for fetch all email without reply"""
        for server in self.filtered(lambda s: s.per_user):
            exist = (
                self.env["mail.channel"]
                .sudo()
                .search(
                    [
                        ("name", "=", "Inbox " + server.user),
                        ("alias_name", "=", server.user),
                    ]
                )
            )
            if not exist:
                self.env["mail.channel"].sudo().create(
                    {"name": "Inbox " + server.user, "alias_name": server.user}
                )

    def button_get_last_uid(self):
        for server in self.filtered(lambda s: s.per_user):
            try:
                imap_server = server.connect()
                massages_count = imap_server.select()
                # Use search(), not status()
                # status, response = imap.search(None, 'INBOX', '(UNSEEN)')
                # unread_msg_nums = response[0].split()
                self.last_uid = int(massages_count[1][0].decode("utf-8")) + 1
            except Exception:
                _logger.info(
                    "Failed to processget last uid %s" % server.name,
                    exc_info=True,
                )

    def fetch_mail(self):
        """WARNING: meant for cron usage only - will commit() after each email!"""
        additionnal_context = {"fetchmail_cron_running": True}
        MailThread = self.env["mail.thread"]
        for server in self.filtered(lambda s: s.per_user):
            _logger.info(
                "start checking for new emails on %s EMAIL PER USER server %s",
                server.server_type,
                server.name,
            )
            additionnal_context["default_fetchmail_server_id"] = server.id

            count, failed = 0, 0
            imap_server = None
            try:
                imap_server = server.connect()
                imap_server.select()

                # Only download new emails
                email_filter = ["(UID %s:*)" % (server.last_uid)]
                data = imap_server.uid("search", None, *email_filter)[1]

                new_max_uid = server.last_uid
                for uid in data[0].split():
                    if int(uid) <= server.last_uid:
                        # We get always minimum 1 message.  If no new message, we receive the newest already managed.
                        continue

                    result, data = imap_server.uid("fetch", uid, "(RFC822)")

                    if not data[0]:
                        continue

                    # SET NOT SEEN
                    if "Seen" in data[1].decode("utf-8"):
                        imap_server.uid("STORE", uid, "-FLAGS", "(\\Seen)")

                    try:
                        res_id = MailThread.with_context(
                            **additionnal_context
                        ).message_process(
                            server.object_id.model,
                            data[0][1],
                            save_original=server.original,
                            strip_attachments=(not server.attach),
                        )
                        new_max_uid = max(new_max_uid, int(uid))
                    except Exception:
                        _logger.info(
                            "Failed to process mail from %s server %s.",
                            server.server_type,
                            server.name,
                            exc_info=True,
                        )
                        failed += 1

                    self._cr.commit()
                    count += 1
                server.write({"last_uid": new_max_uid})
                _logger.info(
                    "Fetched %d email(s) on %s server %s; %d succeeded, %d failed.",
                    count,
                    server.server_type,
                    server.name,
                    (count - failed),
                    failed,
                )
            except Exception:
                _logger.info(
                    "General failure when trying to fetch mail from %s server %s.",
                    server.server_type,
                    server.name,
                    exc_info=True,
                )
            finally:
                if imap_server:
                    imap_server.close()
                    imap_server.logout()
                server.write({"date": fields.Datetime.now()})
        return super(
            FetchmailServer, self.filtered(lambda s: not s.per_user)
        ).fetch_mail()
