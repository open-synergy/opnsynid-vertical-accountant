# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Accountant Firm Partner Arrangement",
    "version": "8.0.2.0.0",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "accountant_app",
        "base_workflow_policy",
        "base_print_policy",
        "base_multiple_approval",
        "base_cancel_reason",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_workflow_policy_data.xml",
        "views/accountant_config_setting_views.xml",
        "views/accountant_partner_arrangement_views.xml",
    ],
    "installable": True,
}
