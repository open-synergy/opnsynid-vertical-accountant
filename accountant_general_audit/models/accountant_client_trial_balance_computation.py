# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval as eval


class AccountantClientTrialBalanceComputation(models.Model):
    _name = "accountant.client_trial_balance_computation"
    _description = "Accountant Client Trial Balance Computation"

    @api.depends(
        "trial_balance_id",
        "computation_item_id",
        "trial_balance_id.standard_detail_ids",
        "trial_balance_id.standard_detail_ids.balance",
        "trial_balance_id.standard_detail_ids.previous_balance",
        "trial_balance_id.standard_detail_ids.extrapolation_balance",
    )
    @api.multi
    def _compute_amount(self):
        obj_computation = self.env["accountant.client_account_type_computation_item"]
        for document in self:
            amount = amount_extrapolation = amount_previous = 0.0
            criteria = [
                ("computation_id", "=", document.computation_item_id.id),
                (
                    "account_type_set_id",
                    "=",
                    document.trial_balance_id.account_type_set_id.id,
                ),
            ]
            computations = obj_computation.search(criteria)
            if len(computations) > 0:
                python_code = computations[0].phyton_code

                localdict = document._get_localdict()
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    amount = localdict["result"]
                    amount_extrapolation = localdict["result_extrapolation"]
                    amount_previous = localdict["result_previous"]
                except Exception:
                    amount = amount_extrapolation = amount_previous = 0.0
            document.amount = amount
            document.amount_extrapolation = amount_extrapolation
            document.amount_previous = amount_previous

    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="accountant.client_trial_balance",
        required=True,
        ondelete="cascade",
    )
    computation_item_id = fields.Many2one(
        string="Computation Item",
        comodel_name="accountant.trial_balance_computation_item",
        required=True,
    )
    amount = fields.Float(
        string="Amount",
        compute="_compute_amount",
        store=True,
    )
    amount_extrapolation = fields.Float(
        string="Amount Extrapolation",
        compute="_compute_amount",
        store=True,
    )
    amount_previous = fields.Float(
        string="Amount Previous",
        compute="_compute_amount",
        store=True,
    )

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }
