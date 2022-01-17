# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author

{
    "name": "Stakeholder Report for Accountant Report",
    "version": "8.0.1.0.0",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "accountant_report",
        "base_sequence_configurator",
        "base_multiple_approval",
        "base_workflow_policy",
        "base_cancel_reason",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/accountant_report_stakeholder_report_type_views.xml",
    ],
    "installable": True,
}
