from odoo import fields, models


class IrMailPopular(models.Model):
    _name = "ir.mail_popular"

    name = fields.Char(string="Description", required=True, index=True)
    sequence = fields.Integer(
        string="Priority",
        default=10,
        help="When no specific mail server is requested for a mail, the highest priority one "
        "is used. Default priority is 10 (smaller number = higher priority)",
    )
    active = fields.Boolean(default=True)

    # OUTGOING SERVER
    smtp_host = fields.Char(
        string="SMTP Server",
        required=True,
        help="Hostname or IP of SMTP server",
    )
    smtp_port = fields.Integer(
        string="SMTP Port",
        required=True,
        default=25,
        help="SMTP Port. Usually 465 for SSL, and 25 or 587 for other cases.",
    )
    smtp_encryption = fields.Selection(
        [("none", "None"), ("starttls", "TLS (STARTTLS)"), ("ssl", "SSL/TLS")],
        string="Connection Security",
        required=True,
        default="none",
        help="Choose the connection encryption scheme:\n"
        "- None: SMTP sessions are done in cleartext.\n"
        "- TLS (STARTTLS): TLS encryption is requested at start of SMTP session (Recommended)\n"
        "- SSL/TLS: SMTP sessions are encrypted with SSL/TLS through a dedicated port (default: 465)",
    )
    smtp_debug = fields.Boolean(
        string="Debugging",
        help="If enabled, the full output of SMTP sessions will "
        "be written to the server log at DEBUG level "
        "(this is very verbose and may include confidential info!)",
    )

    # INCOMING SERVER
    imap_host = fields.Char(
        string="IMAP Server",
        required=True,
        help="Hostname or IP of SMTP server",
    )
    imap_port = fields.Integer(
        string="IMAP Port",
        required=True,
        default=995,
    )
    imap_encryption = fields.Boolean(
        "SSL/TLS",
        help="Connections are encrypted with SSL/TLS through a dedicated port (default: IMAPS=993, POP3S=995)",
    )
