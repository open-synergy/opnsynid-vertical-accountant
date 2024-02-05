{
    "name": "Manage Accountant Report",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_accountant",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_ready_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_duration_mixin",
        "ssi_m2o_configurator_mixin",
        "ssi_res_partner_m2o_configurator_mixin",
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
        "menu.xml",
        "views/accountant_service_views.xml",
        "views/accountant_report_mixin_views.xml",
        "views/accountant_assurance_report_views.xml",
        "views/accountant_nonassurance_report_views.xml",
    ],
}
