# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "General Audit Worksheet RA.220",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_accountant_general_audit",
        "ssi_accountant_general_audit_ws_ra150",
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
        "data/accountant_general_audit_worksheet_conclusion_data.xml",
        "data/accountant_assersion_type_data.xml",
        "views/ws_ra220_views.xml",
        "views/ws_ra2201_views.xml",
        "views/ws_ra22011_views.xml",
        "views/ws_ra22012_views.xml",
        "views/ws_ra2202_views.xml",
        "views/ws_ra22021_views.xml",
        "views/ws_ra2203_views.xml",
    ],
    "demo": [],
}
