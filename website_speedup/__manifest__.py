# Copyright 2020-2022 Artem Shurshilov
# License OPL-1.0

{
    "name": "Speedup Website",
    "summary": """Optimize website odoo core
Speed up your website, zip js bundle, reduce js bundle
zip bundle

""",
    "category": "Website",
    "version": "0.0.0",
    "author": "EURO ODOO, Shurshilov Artem",
    "license": "OPL-1",
    "website": "https://eurodoo.com",
    "price": 49,
    "currency": "EUR",
    "depends": ["website"],
    "images": [
        "static/description/compress.png",
    ],
    "installable": False,
    "assets": {
        "web.assets_common": [
            (
                "replace",
                "web/static/lib/moment/moment.js",
                "website_speedup/static/lib/moment.min.js",
            ),
            (
                "replace",
                "web/static/lib/underscore/underscore.js",
                "website_speedup/static/lib/underscore-min.js",
            ),
            (
                "replace",
                "web/static/lib/jquery/jquery.js",
                "website_speedup/static/lib/jquery.min.js",
            ),
            (
                "replace",
                "web/static/lib/jquery.ui/jquery-ui.js",
                "website_speedup/static/lib/jquery-ui.min.js",
            ),
            (
                "replace",
                "web/static/lib/underscore.string/lib/underscore.string.js",
                "website_speedup/static/lib/underscore.string.min.js",
            ),
            (
                "replace",
                "web/static/lib/select2/select2.js",
                "website_speedup/static/lib/select2.min.js",
            ),
            (
                "replace",
                "web/static/lib/jquery.ba-bbq/jquery.ba-bbq.js",
                "website_speedup/static/lib/jquery.ba-bbq.min.js",
            ),
            (
                "replace",
                "web/static/lib/jquery.form/jquery.form.js",
                "website_speedup/static/lib/jquery.form.min.js",
            ),
            # (
            #     "replace",
            #     "web/static/lib/popper/popper.js",
            #     "website_speedup/static/lib/bootstrap.min.js",
            # ),
            # If not in use, you can also disable
            # ('remove', 'web/static/lib/bootstrap/js/alert.js'),
            # ('remove', 'web/static/lib/bootstrap/js/button.js'),
            # ('remove', 'web/static/lib/bootstrap/js/carousel.js'),
            # ('remove', 'web/static/lib/bootstrap/js/collapse.js'),
            # ('remove', 'web/static/lib/bootstrap/js/dropdown.js'),
            # ('remove', 'web/static/lib/bootstrap/js/index.js'),
            # ('remove', 'web/static/lib/bootstrap/js/modal.js'),
            # ('remove', 'web/static/lib/bootstrap/js/popover.js'),
            # ('remove', 'web/static/lib/bootstrap/js/scrollspy.js'),
            # ('remove', 'web/static/lib/bootstrap/js/tab.js'),
            # ('remove', 'web/static/lib/bootstrap/js/toast.js'),
            # ('remove', 'web/static/lib/bootstrap/js/tooltip.js'),
            # ('remove', 'web/static/lib/bootstrap/js/util.js'),
            (
                "replace",
                "web/static/lib/tempusdominus/tempusdominus.js",
                "website_speedup/static/lib/tempusdominus-bootstrap-4.min.js",
            ),
        ]
    },
}
