# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Accountant Report + Operating Unit",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_accountant_report",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/assurance_report.xml",
        "security/res_group/nonassurance_report.xml",
        "security/ir_rule/assurance_report.xml",
        "security/ir_rule/nonassurance_report.xml",
        "views/assurance_report_views.xml",
        "views/nonassurance_report_views.xml",
    ],
    "demo": [],
}
