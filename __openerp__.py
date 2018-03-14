# -*- coding: utf-8 -*-
{
    'name': "payment_cost",

    'summary': """
        Funcionalidad para generar un costo al enviar dinero.""",

    'description': """
        Cuando enviamos dinero a un proveedor podemos generar un costo fijo o porcentaje
        del monto enviado (gasto).
        Cuando enviamos dinero a un cliente podemos generar un costo para la empresa, es
        decir, un descuento al cliente.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}