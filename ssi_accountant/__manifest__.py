# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Accountant",
    "version": "14.0.2.3.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "configuration_helper",
        "ssi_master_data_mixin",
        "product",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "menu.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_industry_views.xml",
        "views/accountant_financial_accounting_standard_views.xml",
        "views/accountant_service_views.xml",
        "views/accountant_opinion_views.xml",
    ],
    "demo": [
        "demo/accountant_opinion_demo.xml",
        "demo/accountant_service_demo.xml",
        "demo/accountant_financial_accounting_standard_demo.xml",
    ],
}
