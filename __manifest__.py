# -*- coding: utf-8 -*-
{
    'name': "jt_website_sale_vatprices",

    'summary': "Display incl/excl VAT prices on website",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",
    "license": "AGPL-3",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'website_sale',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/website_sale_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'jt_website_sale_vatprices/static/src/js/**/*',
        ],
    },        
}
