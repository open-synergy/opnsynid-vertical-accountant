# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet PE.110",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_accountant_general_audit",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        # "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "data/accountant_general_audit_worksheet_type_data.xml",
        "views/accountant_general_audit_ws_pe110_views.xml",
        "views/accountant_general_audit_ws_pe1101_views.xml",
        "views/accountant_general_audit_ws_pe1102_views.xml",
        "views/accountant_general_audit_ws_pe11021_views.xml",
        "views/accountant_general_audit_ws_pe11022_views.xml",
        "views/accountant_general_audit_ws_pe1103_views.xml",
        "views/accountant_general_audit_ws_pe1104_views.xml",
    ],
    "demo": [
        # "demo/accountant_financial_accounting_standard_demo.xml",
        # "demo/accountant_client_account_type_set_demo.xml",
        # "demo/accountant_client_account_demo.xml",
    ],
}
