# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Copyright 2018 Artem Shurshilov, Eyekraft


{
    'name': 'Subtask notebook page in project task',
    'category': 'project',
    'description': """
Расширяет форму задачи из модуля проекты, добавляя новую страницу в блокноте (page in notebook html) с сабтасками
""",
    'depends': [
        'project',
        'hr_timesheet',
    ],
    'author': "Shurshilov Artem",
    'website': "http://www.eurodoo.com",
    'version': '10.0.0.1',
    'images': [
        'static/description/screen.png',
    ],
    'data': [
        'project_timesheet_view.xml',
    ],
    'application': False,
}

