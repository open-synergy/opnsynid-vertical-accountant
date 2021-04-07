# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Accountant Service App",
    "summary": "Manage Accountancy Service",
    "version": "8.0.1.1.0",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "wizards/convert_product_to_service.xml",
        "views/accountant_config_setting_views.xml",
        "views/accountant_service_views.xml",
    ],
    "installable": True,
    "application": True,
}
