# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author/

{
    "name": "Accountant General Audit",
    "version": "8.0.2.4.0",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_print_policy",
        "base_multiple_approval",
        "base_cancel_reason",
        "base_custom_information",
        "accountant_app",
        "web_readonly_bypass",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "menu.xml",
        "views/accountant_client_account_type_set_views.xml",
        "views/accountant_client_account_type_views.xml",
        "views/accountant_client_trial_balance_views.xml",
        "views/accountant_trial_balance_computation_item_views.xml",
        "views/accountant_financial_accounting_standard_views.xml",
        "views/accountant_general_audit_views.xml",
    ],
    "demo": [
        "demo/accountant_financial_accounting_standard_demo.xml",
        "demo/accountant_client_account_type_demo.xml",
        "demo/accountant_client_account_type_set_demo.xml",
    ],
    "installable": True,
}
