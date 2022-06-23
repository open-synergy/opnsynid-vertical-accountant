# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Manage Accountant Report",
    "version": "8.0.2.4.0",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "accountant_app",
        "web_readonly_bypass",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "data/ir_sequence_data.xml",
        "views/accountant_config_setting_views.xml",
        "views/accountant_report_opinion_views.xml",
        "views/accountant_report_method_views.xml",
        "views/accountant_service_views.xml",
        "views/accountant_report_views.xml",
    ],
    "installable": True,
}
