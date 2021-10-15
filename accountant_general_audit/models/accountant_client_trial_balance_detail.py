# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantClientTrialBalanceDetail(models.Model):
    _name = "accountant.client_trial_balance_detail"
    _description = "Accountant Client Trial Balance Detail"
    _order = "sequence, trial_balance_id, id"

    @api.depends(
        "adjustment_detail_ids",
        "adjustment_detail_ids.debit",
        "adjustment_detail_ids.credit",
    )
    def _compute_audited(self):
        for record in self:
            account = record.account_id
            debit = credit = adjustment = audited = 0.0
            for adj in record.adjustment_detail_ids:
                debit += adj.debit
                credit += adj.credit
            if account.normal_balance == "dr":
                adjustment = debit - credit
            else:
                adjustment = credit - debit
            audited = record.balance + adjustment
            record.adjustment_balance = adjustment
            record.audited_balance = audited

    account_id = fields.Many2one(
        string="Account",
        comodel_name="accountant.client_account",
        required=True,
        ondelete="restrict",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="account_id.sequence",
        store=True,
    )
    previous_balance = fields.Float(
        string="Previous Balance",
        required=True,
    )
    balance = fields.Float(
        string="Home Statement Balance",
        required=True,
    )
    interim_balance = fields.Float(
        string="Interim Balance",
        required=True,
    )
    adjustment_balance = fields.Float(
        string="Adjustment Balance",
        compute="_compute_audited",
        store=True,
    )
    audited_balance = fields.Float(
        string="Audited Balance",
        compute="_compute_audited",
        store=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        related="account_id.type_id",
        store=True,
    )
    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
        ondelete="cascade",
    )
    adjustment_detail_ids = fields.One2many(
        string="Adjustment Detail",
        comodel_name="accountant.client_adjustment_entry_detail",
        inverse_name="trial_balance_detail_id",
    )
