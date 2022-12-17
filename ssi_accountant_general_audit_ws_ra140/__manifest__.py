# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet RA.140",
    "version": "14.0.1.6.0",
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
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "data/accountant_general_audit_worksheet_type_data.xml",
        "data/accountant_financial_ratio_data.xml",
        "views/accountant_client_account_type_views.xml",
        "views/accountant_analytic_procedure_conclusion_category_views.xml",
        "views/accountant_financial_ratio_views.xml",
        "views/ws_ra140_views.xml",
        "views/ws_ra1401_views.xml",
        "views/ws_ra1402_views.xml",
    ],
    "demo": [],
}
