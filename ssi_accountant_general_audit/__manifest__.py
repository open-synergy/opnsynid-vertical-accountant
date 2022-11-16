# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Accountant General Audit",
    "version": "14.0.1.8.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_accountant",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_open_mixin",
        "ssi_project",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_accountant_general_report_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "data/accountant_client_account_group_data.xml",
        "data/accountant_client_account_type_data.xml",
        "data/accountant_trial_balance_computation_item_data.xml",
        "data/accountant_general_audit_worksheet_type_category_data.xml",
        "menu.xml",
        "wizards/import_trial_balance_detail.xml",
        "views/accountant_general_audit_opinion_views.xml",
        "views/accountant_client_account_group_views.xml",
        "views/accountant_client_account_type_views.xml",
        "views/accountant_client_account_views.xml",
        "views/accountant_trial_balance_computation_item_views.xml",
        "views/accountant_client_account_type_set_views.xml",
        "views/accountant_general_audit_worksheet_type_category_views.xml",
        "views/accountant_general_audit_worksheet_type_views.xml",
        "views/accountant_general_audit_worksheet_conclusion_views.xml",
        "views/accountant_general_audit_standard_detail_views.xml",
        "views/accountant_general_audit_group_detail_views.xml",
        "views/accountant_general_audit_computation_views.xml",
        "views/accountant_general_audit_views.xml",
        "views/accountant_client_trial_balance_detail_views.xml",
        "views/accountant_client_trial_balance_standard_detail_views.xml",
        "views/accountant_client_trial_balance_group_detail_views.xml",
        "views/accountant_client_trial_balance_computation_views.xml",
        "views/accountant_client_trial_balance_views.xml",
        "views/accountant_client_adjustment_entry_views.xml",
        "views/accountant_general_audit_worksheet_mixin_views.xml",
    ],
    "demo": [
        "demo/accountant_financial_accounting_standard_demo.xml",
        "demo/accountant_client_account_type_set_demo.xml",
        "demo/accountant_client_account_demo.xml",
    ],
}
