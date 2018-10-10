# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Manage Accountant Report",
    "version": "8.0.1.4.2",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "license": "AGPL-3",
    "depends": [
        "accountant_app",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_module_category_data.xml",
        "data/ir_sequence_data.xml",
        "views/accountant_config_setting_views.xml",
        "views/accountant_report_opinion_views.xml",
        "views/accountant_service_views.xml",
        "views/accountant_report_views.xml",
    ],
    "installable": True,
}
