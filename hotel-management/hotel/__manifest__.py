# -*- coding: utf-8 -*-
{
    'name': "hotel",
    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,
    'author': "Diary",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/customer_demo_data.xml',
        'data/equipment_data.xml',
        'data/room_category_data.xml',
        'views/equipment_views.xml',
        'views/room_category_views.xml',
        'views/room_views.xml',
        'views/room_reservation_views.xml',
        'views/templates.xml',
        'views/template_landing_page.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
}

