# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# Copyright 2017-2018 Artem Shurshilov
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from . import wizards
from . import models

def post_load():
    from .models import binary_fields
    from .models import image
