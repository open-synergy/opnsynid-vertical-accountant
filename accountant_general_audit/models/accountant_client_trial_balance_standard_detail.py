# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from openerp import api, fields, models
from openerp.tools.safe_eval import (  # pylint: disable=redefined-builtin
    safe_eval as eval,
)


class AccountantClientTrialBalanceStandardDetail(models.Model):
    _name = "accountant.client_trial_balance_standard_detail"
    _description = "Accountant Client Trial Balance Standard Detail"
    _order = "sequence, trial_balance_id, id"

    @api.depends(
        "trial_balance_id",
        "trial_balance_id.date_start",
        "trial_balance_id.date_end",
        "trial_balance_id.previous_date_start",
        "trial_balance_id.previous_date_end",
        "trial_balance_id.interim_date_start",
        "trial_balance_id.interim_date_end",
        "type_id",
        "trial_balance_id.detail_ids",
        "trial_balance_id.detail_ids.type_id",
        "trial_balance_id.detail_ids.previous_balance",
        "trial_balance_id.detail_ids.balance",
        "trial_balance_id.detail_ids.interim_balance",
    )
    @api.multi
    def _compute_balance(self):
        obj_detail = self.env["accountant.client_trial_balance_detail"]
        for document in self:
            previous_balance = balance = interim_balance = extrapolation_balance = 0.0

            criteria = [
                ("trial_balance_id", "=", document.trial_balance_id.id),
                ("type_id", "=", document.type_id.id),
            ]
            for detail in obj_detail.search(criteria):
                previous_balance += detail.previous_balance
                balance += detail.balance
                interim_balance += detail.interim_balance
            localdict = document._get_localdict(
                previous_balance,
                balance,
                interim_balance,
            )
            try:
                eval(
                    document.type_id.extrapolation_python_code,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                extrapolation_balance = localdict["result"]
            except Exception:
                extrapolation_balance = 7.0
            document.previous_balance = previous_balance
            document.balance = balance
            document.extrapolation_balance = extrapolation_balance

    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    previous_balance = fields.Float(
        string="Previous Balance",
        required=False,
        compute="_compute_balance",
        store=True,
    )
    balance = fields.Float(
        string="Balance",
        required=False,
        compute="_compute_balance",
        store=True,
    )
    extrapolation_balance = fields.Float(
        string="Extrapolation Balance",
        required=False,
        compute="_compute_balance",
        store=True,
    )
    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
        ondelete="cascade",
    )

    def _get_localdict(self, previous_balance, balance, interim_balance):
        self.ensure_one()
        tb = self.trial_balance_id
        date_start = (
            tb.date_start and datetime.strptime(tb.date_start, "%Y-%m-%d") or False
        )
        date_end = tb.date_end and datetime.strptime(tb.date_end, "%Y-%m-%d") or False
        previous_date_start = (
            tb.previous_date_start
            and datetime.strptime(tb.previous_date_start, "%Y-%m-%d")
            or False
        )
        previous_date_end = (
            tb.previous_date_end
            and datetime.strptime(tb.previous_date_end, "%Y-%m-%d")
            or False
        )
        interim_date_start = (
            tb.interim_date_start
            and datetime.strptime(tb.interim_date_start, "%Y-%m-%d")
            or False
        )
        interim_date_end = (
            tb.interim_date_end
            and datetime.strptime(tb.interim_date_end, "%Y-%m-%d")
            or False
        )
        return {
            "env": self.env,
            "document": self,
            "previous_balance": previous_balance,
            "interim_balance": interim_balance,
            "balance": balance,
            "datetime": datetime,
            "date_start": date_start,
            "date_end": date_end,
            "previous_date_start": previous_date_start,
            "previous_date_end": previous_date_end,
            "interim_date_start": interim_date_start,
            "interim_date_end": interim_date_end,
        }
