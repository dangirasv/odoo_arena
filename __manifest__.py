# -*- coding: utf-8 -*-
{
    'name': "odooarena",

    'summary': """
        A simple 1v1 rpg style Battle Arena game using Odoo's framework""",

    'description': """
        Your characters battles through various different characters (each stronger the more wins you get). You collect
        items after each win and upgrade your character.
    """,

    'author': "Dangiras Venckus",
    'website': "http://www.odooarena.tk",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}