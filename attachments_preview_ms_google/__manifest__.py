# -*- coding: utf-8 -*-
# Copyright (C) 2020 Artem Shurshilov <shurshilov.a@yandex.ru>
# Odoo Proprietary License v1.0

# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps, or if you have received a written
# agreement from the authors of the Software (see the COPYRIGHT file).

# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).

# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.

# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
{
    'name': "Preview attachment in MS and Google online",

    'summary': """
        Image files (.JPEG, .PNG, .GIF, .TIFF, .BMP)
        Video files (WebM, .MPEG4, .3GPP, .MOV, .AVI, .MPEGPS, .WMV, .FLV)
        Text files (.TXT)
        Markup/Code (.CSS, .HTML, .PHP, .C, .CPP, .H, .HPP, .JS)
        Microsoft Word (.DOC and .DOCX)
        Microsoft Excel (.XLS and .XLSX)
        Microsoft PowerPoint (.PPT and .PPTX)
        Adobe Portable Document Format (.PDF)
        Apple Pages (.PAGES)
        Adobe Illustrator (.AI)
        Adobe Photoshop (.PSD)
        Tagged Image File Format (.TIFF)
        Autodesk AutoCad (.DXF)
        Scalable Vector Graphics (.SVG)
        PostScript (.EPS, .PS)
        TrueType (.TTF)
        XML Paper Specification (.XPS)
        Archive file types (.ZIP and .RAR)
        """,

    'author': "Shurshilov Artem",
    'website': "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com/login_employee?login=demo1&amp;password=demo1",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point Of Sale',
    'version': '13.0.0.0',
    "license": "OPL-1",
    # 'price': 29,
    # 'currency': 'EUR',
    'images':[
        'static/description/Microsoft and Google preview.gif',
        'static/description/button_url.png',
        'static/description/button_manage_search.png',
        'static/description/button_download.png',
    ],

    # any module necessary for this one to work correctly
    'depends': ['base','web', 'mail'],
    'installable': True,

    # always loaded
    'data': [
        'views/assets.xml',
    ],

    'qweb': [
        'static/src/xml/attachments_preview_ms_and_google.xml',
    ],
}
