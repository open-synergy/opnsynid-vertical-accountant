# -*- coding: utf-8 -*-
# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantGeneralAuditIndexA2201Detail(models.Model):
    _name = "accountant.general_audit_index_a2201_detail"
    _description = "Accountant General Audit Index A.220.1 Details"
    _order = "sequence, index_a2201_id, id"

    @api.multi
    @api.depends(
        "balance",
        "extrapolation_balance",
        "previous_balance",
    )
    def _compute_amount(self):
        for document in self:
            extrapolation_previous_change_amount = (
                extrapolation_previous_change_percentage
            ) = (
                balance_previous_change_amount
            ) = balance_previous_change_change_percentage = 0.0
            extrapolation_previous_change_amount = (
                document.extrapolation_balance - document.previous_balance
            )
            try:
                extrapolation_previous_change_percentage = (
                    document.extrapolation_balance / document.previous_balance
                ) * 100.0
            except Exception:
                extrapolation_previous_change_percentage = 0.0
            balance_previous_change_amount = (
                document.balance - document.previous_balance
            )
            try:
                balance_previous_change_change_percentage = (
                    document.balance / document.previous_balance
                ) * 100.0
            except Exception:
                balance_previous_change_change_percentage = 0.0
            document.extrapolation_previous_change_amount = (
                extrapolation_previous_change_amount
            )
            document.extrapolation_previous_change_percentage = (
                extrapolation_previous_change_percentage
            )
            document.balance_previous_change_amount = balance_previous_change_amount
            document.balance_previous_change_change_percentage = (
                balance_previous_change_change_percentage
            )

    @api.multi
    @api.depends(
        "balance",
        "extrapolation_balance",
        "previous_balance",
    )
    def _compute_percentage(self):
        obj_computation = self.env["accountant.client_trial_balance_computation"]
        for document in self:
            percentage = percentage_extrapolation = percentage_previous = 0.0
            bottom_line = document.type_id.bottom_line_id
            tb = document.general_audit_id.trial_balance_id
            if bottom_line and tb:
                criteria = [
                    ("computation_item_id", "=", bottom_line.id),
                    ("trial_balance_id", "=", tb.id),
                ]
                computations = obj_computation.search(criteria)
                if len(computations) > 0:
                    bottom_line_amount = computations[0].amount
                    bottom_line_amount_extrapolation = computations[
                        0
                    ].amount_extrapolation
                    bottom_line_amount_previous = computations[0].amount_previous
                    try:
                        percentage = document.balance / bottom_line_amount
                    except Exception:
                        percentage = 0.0
                    try:
                        percentage_extrapolation = (
                            document.extrapolation_balance
                            / bottom_line_amount_extrapolation
                        )
                    except Exception:
                        percentage_extrapolation = 0.0
                    try:
                        percentage_previous = (
                            document.previous_balance / bottom_line_amount_previous
                        )
                    except Exception:
                        percentage_previous = 0.0
            document.percentage = percentage
            document.percentage_extrapolation = percentage_extrapolation
            document.percentage_previous = percentage_previous

    index_a2201_id = fields.Many2one(
        string="# Index A.220.1",
        comodel_name="accountant.general_audit_index_a2201",
        required=True,
        ondelete="cascade",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="accountant.client_trial_balance_standard_detail",
        required=True,
    )
    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="accountant.client_account_type",
        related="standard_detail_id.type_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="standard_detail_id.sequence",
        store=True,
    )
    balance = fields.Float(
        string="Balance",
        related="standard_detail_id.balance",
        store=True,
    )
    extrapolation_balance = fields.Float(
        string="Extrapolation Balance",
        related="standard_detail_id.extrapolation_balance",
        store=True,
    )
    previous_balance = fields.Float(
        string="Previous Balance",
        related="standard_detail_id.previous_balance",
        store=True,
    )
    percentage = fields.Float(
        string="Percentage",
        compute="_compute_percentage",
        store=True,
    )
    percentage_extrapolation = fields.Float(
        string="Percentage (Extrapolation)",
        compute="_compute_percentage",
        store=True,
    )
    percentage_previous = fields.Float(
        string="Percentage (Previous)",
        compute="_compute_percentage",
        store=True,
    )
    extrapolation_previous_change_amount = fields.Float(
        string="Extrapolation - Previous",
        compute="_compute_amount",
        store=True,
    )
    extrapolation_previous_change_percentage = fields.Float(
        string="Extrapolation - Previous (Percentage)",
        compute="_compute_amount",
        store=True,
    )
    balance_previous_change_amount = fields.Float(
        string="Balance - Previous",
        compute="_compute_amount",
        store=True,
    )
    balance_previous_change_change_percentage = fields.Float(
        string="Balance - Previous (Percentage)",
        compute="_compute_amount",
        store=True,
    )
    industry_average = fields.Float(
        string="Industry Average",
    )
    note = fields.Text(
        string="Note",
    )
