# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author

{
    "name": "BPK Stakeholder Report for Accountant Report",
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
        "views/accountant_report_stakeholder_report_bpk_views.xml",
    ],
    "installable": True,
}
