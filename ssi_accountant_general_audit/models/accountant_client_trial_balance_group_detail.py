# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import api, fields, models


class AccountantClientTrialBalanceGroupDetail(models.Model):
    _name = "accountant.client_trial_balance_group_detail"
    _description = "Accountant Client Trial Balance Group Detail"
    _order = "sequence, trial_balance_id, id"

    @api.depends(
        "trial_balance_id",
        "trial_balance_id.date_start",
        "trial_balance_id.date_end",
        "trial_balance_id.previous_date_start",
        "trial_balance_id.previous_date_end",
        "trial_balance_id.interim_date_start",
        "trial_balance_id.interim_date_end",
        "group_id",
        "trial_balance_id.standard_detail_ids",
        "trial_balance_id.standard_detail_ids.type_id",
        "trial_balance_id.standard_detail_ids.balance",
    )
    def _compute_balance(self):
        StdDetail = self.env["accountant.client_trial_balance_standard_detail"]
        for document in self:
            balance = 0.0
            criteria = [
                ("trial_balance_id", "=", document.trial_balance_id.id),
                ("type_id.group_id.id", "=", document.group_id.id),
            ]
            for detail in StdDetail.search(criteria):
                balance += detail.balance
            document.balance = balance

    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
        ondelete="cascade",
    )
    group_id = fields.Many2one(
        string="Account Group",
        comodel_name="accountant.client_account_group",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="trial_balance_id.currency_id",
        store=True,
    )
    balance = fields.Monetary(
        string="Balance",
        required=False,
        compute="_compute_balance",
        store=True,
        currency_field="currency_id",
    )
