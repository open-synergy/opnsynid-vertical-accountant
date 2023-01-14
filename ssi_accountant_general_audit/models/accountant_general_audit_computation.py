# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class AccountantGeneralAuditComputation(models.Model):
    _name = "accountant.general_audit_computation"
    _description = "Accountant General Audit Computation"

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        required=True,
        ondelete="cascade",
    )
    computation_item_id = fields.Many2one(
        string="Computation Item",
        comodel_name="accountant.trial_balance_computation_item",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="computation_item_id.sequence",
    )

    @api.depends(
        "general_audit_id",
        "general_audit_id.home_trial_balance_id",
        "general_audit_id.interim_trial_balance_id",
        "general_audit_id.previous_trial_balance_id",
    )
    def _compute_computation(self):
        Computation = self.env["accountant.client_trial_balance_computation"]
        for record in self:
            home_result = interim_result = previous_result = False
            criteria = [
                ("computation_item_id", "=", record.computation_item_id.id),
            ]
            if record.general_audit_id.home_trial_balance_id:
                criteria_home = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.home_trial_balance_id.id,
                    )
                ]
                home_results = Computation.search(criteria_home)
                if len(home_results) > 0:
                    home_result = home_results[0]

            if record.general_audit_id.interim_trial_balance_id:
                criteria_interim = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.interim_trial_balance_id.id,
                    )
                ]
                interim_results = Computation.search(criteria_interim)
                if len(interim_results) > 0:
                    interim_result = interim_results[0]

            if record.general_audit_id.previous_trial_balance_id:
                criteria_previous = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.previous_trial_balance_id.id,
                    )
                ]
                previous_results = Computation.search(criteria_previous)
                if len(previous_results) > 0:
                    previous_result = previous_results[0]

            record.home_computation_id = home_result
            record.interim_computation_id = interim_result
            record.previous_computation_id = previous_result

    home_computation_id = fields.Many2one(
        string="Home Statement Computation",
        comodel_name="accountant.client_trial_balance_computation",
        readonly=True,
        compute="_compute_computation",
        store=True,
    )
    interim_computation_id = fields.Many2one(
        string="Interim Computation",
        comodel_name="accountant.client_trial_balance_computation",
        readonly=True,
        compute="_compute_computation",
        store=True,
    )
    previous_computation_id = fields.Many2one(
        string="Previous Computation",
        comodel_name="accountant.client_trial_balance_computation",
        readonly=True,
        compute="_compute_computation",
        store=True,
    )
    home_amount = fields.Float(
        string="Home Statement Amount",
        related="home_computation_id.amount",
        store=True,
    )
    extrapolation_amount = fields.Float(
        string="Extrapolation Amount",
        related=False,
        store=True,
    )
    interim_amount = fields.Float(
        string="Interim Amount",
        related="interim_computation_id.amount",
        store=True,
    )
    previous_amount = fields.Float(
        string="Previous Amount",
        related="previous_computation_id.amount",
        store=True,
    )

    @api.depends(
        "home_amount",
        "extrapolation_amount",
        "interim_amount",
        "previous_amount",
    )
    def _compute_average(self):
        for record in self:
            extrapolation = interim = home = 0.0
            extrapolation = (record.extrapolation_amount + record.previous_amount) / 2.0
            interim = (record.interim_amount + record.previous_amount) / 2.0
            home = (record.home_amount + record.previous_amount) / 2.0

            record.extrapolation_avg_amount = extrapolation
            record.interim_avg_amount = interim
            record.home_avg_amount = home

    extrapolation_avg_amount = fields.Float(
        string="Extrapolation Avg. Amount",
        compute="_compute_average",
        store=True,
    )
    interim_avg_amount = fields.Float(
        string="Interim Avg. Amount",
        compute="_compute_average",
        store=True,
    )
    home_avg_amount = fields.Float(
        string="Home Statement Avg. Amount",
        compute="_compute_average",
        store=True,
    )

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
            "tb": self.interim_standard_line_id.trial_balance_id,
        }

    def _get_extrapolation_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _recompute_extrapolation(self, additional_dict):
        self.ensure_one()
        Computation = self.env["accountant.client_account_type_computation_item"]
        amount = 0.0
        criteria = [
            ("computation_id", "=", self.computation_item_id.id),
            (
                "account_type_set_id",
                "=",
                self.general_audit_id.account_type_set_id.id,
            ),
        ]
        computations = Computation.search(criteria)
        if len(computations) > 0:
            computation = computations[0]
            if computation.use_default:
                python_code = computation.computation_id.python_code
            else:
                python_code = computations[0].python_code

            localdict = self._get_extrapolation_localdict()
            localdict.update(additional_dict)
            try:
                eval(
                    python_code,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                amount = localdict["result"]
                additional_dict.update({self.computation_item_id.code: amount})
            except Exception:
                amount = 0.0
        self.write(
            {
                "extrapolation_amount": amount,
            }
        )
        return additional_dict
