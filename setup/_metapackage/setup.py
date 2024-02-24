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
        'odoo14-addon-ssi_accountant_report_project',
        'odoo14-addon-ssi_accountant_report_work_log',
        'odoo14-addon-ssi_accountant_stakeholder_report',
        'odoo14-addon-ssi_assurance_report_custom_information',
        'odoo14-addon-ssi_assurance_report_quality_control',
        'odoo14-addon-ssi_assurance_report_related_attachment',
        'odoo14-addon-ssi_assurance_report_state_change_constrain',
        'odoo14-addon-ssi_non_assurance_report_custom_information',
        'odoo14-addon-ssi_non_assurance_report_quality_control',
        'odoo14-addon-ssi_non_assurance_report_related_attachment',
        'odoo14-addon-ssi_non_assurance_report_state_change_constrain',
        'odoo14-addon-ssi_partner_identification_accountant_certification',
        'odoo14-addon-ssi_partner_identification_cpa_firm_license',
        'odoo14-addon-ssi_partner_identification_cpa_license',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
