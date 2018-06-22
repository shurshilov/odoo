# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2018 Shurshilov Artem (shurshilov.a@yandex.ru)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'URL attachment',
    'version': '11.0.1.0.0',
    'category': 'Tools',
    'description': """
Module that allows to attach an URL as a document.
    """,
    'author': "Shurshilov Artem",
    'website': "https://vk.com/id20132180",
    'license': 'AGPL-3',
    'depends': [
        'document',
    ],
    'images':[
            'static/description/stock_open2.png',
            'static/description/stock_open.png',
            'static/description/stock_cursor.png',
    ],
    'data': [
        'view/document_url_view.xml',
    ],
    'qweb': [
        'static/src/xml/url.xml',
    ],
    "installable": True,
}
