# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class AccountantClientTrialBalanceComputation(models.Model):
    _name = "accountant.client_trial_balance_computation"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Client Trial Balance Computation"

    @api.depends(
        "trial_balance_id",
        "computation_item_id",
        "trial_balance_id.standard_detail_ids",
        "trial_balance_id.standard_detail_ids.balance",
        "trial_balance_id.standard_detail_ids.previous_balance",
        "trial_balance_id.standard_detail_ids.extrapolation_balance",
        "trial_balance_id.standard_detail_ids.audited_balance",
    )
    def _compute_amount(self):
        obj_computation = self.env["accountant.client_account_type_computation_item"]
        for document in self:
            amount = amount_extrapolation = amount_previous = amount_audited = 0.0
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
                    amount_audited = localdict["result_audited"]
                except Exception:
                    amount = (
                        amount_extrapolation
                    ) = amount_previous = amount_audited = 0.0
            document.amount = amount
            document.amount_extrapolation = amount_extrapolation
            document.amount_previous = amount_previous
            document.amount_audited = amount_audited

    name = fields.Char(
        required=False,
    )
    code = fields.Char(
        required=False,
    )
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
        string="Home Statement Amount",
        compute="_compute_amount",
        store=True,
    )
    amount_extrapolation = fields.Float(
        string="Extrapolation Amount",
        compute="_compute_amount",
        store=True,
    )
    amount_previous = fields.Float(
        string="Previous Amount",
        compute="_compute_amount",
        store=True,
    )
    amount_audited = fields.Float(
        string="Audited Amount",
        compute="_compute_amount",
        store=True,
    )

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def action_recompute(self):
        for record in self:
            record._compute_amount()
