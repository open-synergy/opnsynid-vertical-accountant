# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Manage Accountant Report",
    "version": "14.0.1.0.0",
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
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_accountant_report_data.xml",
        "data/policy_template_accountant_report_data.xml",
        "data/approval_template_accountant_report_data.xml",
        "views/accountant_report_opinion_views.xml",
        "views/accountant_report_method_views.xml",
        "views/accountant_service_views.xml",
        "views/accountant_report_views.xml",
    ],
}
