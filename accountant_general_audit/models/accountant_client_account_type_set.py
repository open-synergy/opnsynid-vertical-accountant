# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAccountTypeSet(models.Model):
    _name = "accountant.client_account_type_set"
    _description = "Accountant Client Account Type Set"

    name = fields.Char(
        string="Account Type Set",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
    )
    detail_ids = fields.Many2many(
        string="Detail",
        comodel_name="accountant.client_account_type",
        relation="rel_accountant_type_set_2_account_type",
        column1="account_client_type_set_id",
        column2="account_client_type_id",
    )
    trial_balance_sequence_id = fields.Many2one(
        string="Trial Balance Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    accountant_type_set_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Account Type Set",
        comodel_name="res.groups",
        relation="rel_accountant_type_set_confirm_trial_balance",
        column1="account_type_set_id",
        column2="group_id",
    )
    accountant_type_set_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval Account Type Set",
        comodel_name="res.groups",
        relation="rel_accountant_type_set_restart_approval_trial_balance",
        column1="account_type_set_id",
        column2="group_id",
    )
    accountant_type_set_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Account Type Set",
        comodel_name="res.groups",
        relation="rel_accountant_type_set_cancel_approval_trial_balance",
        column1="account_type_set_id",
        column2="group_id",
    )
    accountant_type_set_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Account Type Set",
        comodel_name="res.groups",
        relation="rel_accountant_type_set_restart_trial_balance",
        column1="account_type_set_id",
        column2="group_id",
    )
