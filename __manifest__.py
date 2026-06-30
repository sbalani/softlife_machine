{
    'name': 'SoftLife Machine Fleet',
    'version': '18.0.1.0.0',
    'summary': 'Soft-serve machine fleet: customer assignment, hoppers, transfers.',
    'description': """
SoftLife Machine Fleet
======================
Central business object for SoftLife soft-serve machines: customer/site
assignment, serving warehouse, base & topping (hopper) configuration,
HACCP-relevant maintenance dates, and transfer/delivery documents.

Other SoftLife modules depend on this:
- softlife_huaxin  : bridges Huaxin telemetry to machine records (by device_imei)
- softlife_haccp   : adds lot traceability, reposicion, recall on top
""",
    'author': 'SoftLife',
    'website': 'https://softlife.es',
    'category': 'Inventory/Inventory',
    'license': 'OPL-1',
    'depends': ['base', 'stock', 'product', 'mail'],
    'data': [
        'security/softlife_machine_security.xml',
        'security/ir.model.access.csv',
        'data/softlife_machine_data.xml',
        'wizards/machine_transfer_wizard_views.xml',
        'views/softlife_machine_views.xml',
        'views/menus.xml',
    ],
    'demo': ['demo/demo.xml'],
    'installable': True,
    'application': True,
}
