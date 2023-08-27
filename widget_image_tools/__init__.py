# Copyright 2016-2017 LasLabs Inc.
# Copyright 2017-2018 Shurshilov Artem
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from . import models, wizards


def post_load():
    # in /controllers/main there is an import from the `mail` module
    # it leads to loading the mail and all its dependencies earlier than the patch in `binary_fields` is applied.
    # That is why the `from . import controller` line is here
    from . import controllers
    from .models import binary_fields, image
