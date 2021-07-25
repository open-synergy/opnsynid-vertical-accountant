# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAccountTypeSet(models.Model):
    _inherit = "accountant.client_account_type_set"

    # general Audit Index
    accountant_general_audit_index_a1101_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Accountant General Audit Index",
        comodel_name="res.groups",
        relation="rel_accountant_type_set_confirm_general_audit_index_a1101",
        column1="account_type_set_id",
        column2="group_id",
    )
    accountant_general_audit_index_a1101_restart_validation_grp_ids = fields.Many2many(
        string="Allow To Restart Validation Accountant General Audit Index",
        comodel_name="res.groups",
        relation="rel_acc_type_set_restart_validation_gen_audit_index_a1101",
        column1="account_type_set_id",
        column2="group_id",
    )
    accountant_general_audit_index_a1101_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Accountant General Audit Index",
        comodel_name="res.groups",
        relation="rel_accountant_type_set_cancel_general_audit_index_a1101",
        column1="account_type_set_id",
        column2="group_id",
    )
    accountant_general_audit_index_a1101_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Accountant General Audit Index",
        comodel_name="res.groups",
        relation="rel_accountant_type_set_restart_general_audit_index_a1101",
        column1="account_type_set_id",
        column2="group_id",
    )
