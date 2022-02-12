# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author

{
    "name": "OJK Stakeholder Report for Accountant Report",
    "version": "8.0.1.0.0",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "accountant_report_stakeholder_report",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/accountant_report_stakeholder_report_type_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/base_workflow_policy_stakeholder_report_ojk_data.xml",
        "views/accountant_report_stakeholder_report_ojk_views.xml",
    ],
    "demo": [
        "demo/tier_definition_demo.xml",
    ],
    "installable": True,
}
