# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author/

{
    "name": "General Audit Index A.230.5",
    "version": "8.0.1.0.0",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "accountant_general_audit",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "data/accountant_general_audit_index_a2305_status_data.xml",
        "views/accountant_client_account_type_set_views.xml",
        "views/accountant_general_audit_index_a2305_status_views.xml",
        "views/accountant_general_audit_index_a2305_views.xml",
        "views/accountant_general_audit_views.xml",
        "views/accountant_relevant_external_factor_category_views.xml",
        "views/accountant_relevant_external_factor_views.xml",
    ],
    "installable": True,
}
