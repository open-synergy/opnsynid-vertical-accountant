# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Stakeholder Report for Accountant Report",
    "version": "14.0.1.0.0",
    "category": "Administration",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_accountant",
        "ssi_accountant_report",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_transaction_done_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/accountant_report_stakeholder_report_type_views.xml",
        "views/accountant_report_stakeholder_report_views.xml",
    ],
}
