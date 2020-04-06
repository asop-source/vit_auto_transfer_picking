# -*- coding: utf-8 -*-
{
    'name': "vit auto int transfer",

    'summary': """
       Automations Transfer dari purchase ke inventory

       """,

    'description': """
      Confirm Button Validate di PO
    """,

    'author': "asopkarawang@gmail.com",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}