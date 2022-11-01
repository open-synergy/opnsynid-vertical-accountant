# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).


from odoo import api, fields, models


class AccountantClientTrialBalanceDetail(models.Model):
    _name = "accountant.client_trial_balance_detail"
    _description = "Accountant Client Trial Balance Detail"
    _order = "sequence, trial_balance_id, id"

    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
        ondelete="cascade",
    )
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
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        related="account_id.type_id",
        store=True,
    )
    debit = fields.Float(
        string="Debit",
        required=True,
        default=0.0,
    )
    credit = fields.Float(
        string="Credit",
        required=True,
        default=0.0,
    )

    @api.depends(
        "debit",
        "credit",
        "account_id",
    )
    def _compute_balance(self):
        for record in self:
            result = 0.0
            if record.account_id:
                if record.account_id.normal_balance == "dr":
                    result = record.debit - record.credit
                else:
                    result = record.credit - record.debit
            record.balance = result

    balance = fields.Float(
        string="Balance",
        compute="_compute_balance",
        store=True,
    )
