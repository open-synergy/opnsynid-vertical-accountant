import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-vertical-accountant",
    description="Meta package for open-synergy-opnsynid-vertical-accountant Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_accountant',
        'odoo14-addon-ssi_accountant_general_audit',
        'odoo14-addon-ssi_accountant_general_audit_ws_pe110',
        'odoo14-addon-ssi_accountant_general_audit_ws_ra120',
        'odoo14-addon-ssi_accountant_general_audit_ws_ra130',
        'odoo14-addon-ssi_accountant_general_audit_ws_ra140',
        'odoo14-addon-ssi_accountant_general_audit_ws_ra150',
        'odoo14-addon-ssi_accountant_general_audit_ws_ra210',
        'odoo14-addon-ssi_accountant_general_audit_ws_ra220',
        'odoo14-addon-ssi_accountant_general_audit_ws_ra230',
        'odoo14-addon-ssi_accountant_general_audit_ws_rr110',
        'odoo14-addon-ssi_accountant_report',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
