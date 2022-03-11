# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Accountant",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "configuration_helper",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/res_config_settings_views.xml",
        "views/accountant_financial_accounting_standard_views.xml",
        "views/accountant_service_views.xml",
    ],
}
