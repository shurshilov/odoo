# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class WebsiteSocial(models.Model):

    _name = "website.social"
    _description = "Website socials networks"

    name = fields.Char(string='Name')
    name_application = fields.Char(string='Name of application link', help="""If this is just a link leave the field empty
        And if you want it to open in the app like for example chat in whatsapp fill in the app name""")
    contact = fields.Char('Contacn number or account nickname', help="""if whataspp example your number +11231112233
        , else if github example link to your repo https://github.com/shurshilov/odoo """)
    style = fields.Char('Social network CSS style for customize')
    class_css = fields.Char('Social network CSS class')
    background = fields.Boolean('Icon with background?', help="Add,remove class no-bg")
    title = fields.Char('Title of icon')
    icon = fields.Char('Icon svg')


class Website(models.Model):

    _inherit = "website"
    _description = "Website"

    social_network_live = fields.Many2many("website.social", string='Website live chat social network')
    position_social_network = fields.Selection([
        ('position:fixed;height:60px;bottom:40px;right: 0px;', 'Right'),
        ('position:fixed;height:60px;bottom:40px;', 'Left'),
        ('height:60px;bottom:40px;right:0px;top:40px;', 'Top right'),
        ('height:60px;bottom:40px;top:40px;', 'Top right'),
    ], required=True, default='position:fixed;height:60px;bottom:40px;right: 0px;')
