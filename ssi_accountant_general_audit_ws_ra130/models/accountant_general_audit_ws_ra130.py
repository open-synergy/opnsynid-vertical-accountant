# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantGeneralWSAuditRA130(models.Model):
    _name = "accountant.general_audit_ws_ra130"
    _description = "General Audit WS RA.130"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra130.worksheet_type_ra130"

    @api.depends(
        "base_computation_amount",
        "base_computation_extrapolation_amount",
        "other_base_amount",
        "performance_materiality_percentage",
        "overall_materiality_percentage",
        "tolerable_misstatement_percentage",
    )
    def _compute_materiality(self):
        for document in self:
            document.overall_materiality = (
                document.overall_materiality_percentage / 100.00
            ) * document.base_computation_amount
            document.overall_materiality_extrapolation = (
                document.overall_materiality_percentage / 100.00
            ) * document.base_computation_extrapolation_amount
            document.performance_materiality = (
                document.performance_materiality_percentage / 100.00
            ) * document.overall_materiality
            document.performance_materiality_extrapolation = (
                document.performance_materiality_percentage / 100.00
            ) * document.overall_materiality_extrapolation
            document.tolerable_misstatement = (
                document.tolerable_misstatement_percentage / 100.00
            ) * document.performance_materiality
            document.tolerable_misstatement_extrapolation = (
                document.tolerable_misstatement_percentage / 100.00
            ) * document.performance_materiality_extrapolation

    @api.depends(
        "general_audit_id",
        "computation_item_id",
        "other_amount_ok",
        "other_base_amount",
    )
    def _compute_base(self):
        Computation = self.env["accountant.general_audit_computation"]
        for document in self:
            general_audit_computation_id = False
            base_computation_amount = base_computation_extrapolation_amount = 0.0
            if document.general_audit_id and document.computation_item_id:
                criteria = [
                    ("general_audit_id.id", "=", document.general_audit_id.id),
                    ("computation_item_id.id", "=", document.computation_item_id.id),
                ]
                computations = Computation.search(criteria)
                if len(computations) > 0:
                    general_audit_computation_id = computations[0]
                    base_computation_amount = general_audit_computation_id.home_amount
                    base_computation_extrapolation_amount = (
                        general_audit_computation_id.interim_amount
                    )
            if document.other_amount_ok:
                base_computation_amount = document.other_base_amount
                base_computation_extrapolation_amount = document.other_base_amount
            document.general_audit_computation_id = general_audit_computation_id
            document.base_computation_amount = base_computation_amount
            document.base_computation_extrapolation_amount = (
                base_computation_extrapolation_amount
            )

    computation_item_id = fields.Many2one(
        string="Computation Item To Use",
        comodel_name="accountant.trial_balance_computation_item",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    general_audit_computation_id = fields.Many2one(
        string="General Audit Computation",
        comodel_name="accountant.general_audit_computation",
        compute="_compute_base",
        store=True,
    )
    base_computation_amount = fields.Monetary(
        string="Base Amount for Materiality Computation",
        compute="_compute_base",
        store=True,
        currency_field="currency_id",
    )
    base_computation_extrapolation_amount = fields.Monetary(
        string="Base Extrapolation Amount for Materiality Computation",
        compute="_compute_base",
        store=True,
        currency_field="currency_id",
    )
    other_amount_ok = fields.Boolean(
        string="Use Other Amount",
        default=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    other_base_amount = fields.Monetary(
        string="Other Base Amount",
        default=0.0,
        required=True,
        readonly=True,
        currency_field="currency_id",
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    overall_materiality_percentage = fields.Float(
        string="Overall Materiality Percentage",
        default=0.0,
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    overall_materiality = fields.Monetary(
        string="Overall Materiality",
        compute="_compute_materiality",
        store=True,
        currency_field="currency_id",
    )
    overall_materiality_extrapolation = fields.Monetary(
        string="Extrapolation Overall Materiality",
        compute="_compute_materiality",
        store=True,
        currency_field="currency_id",
    )
    overall_materiality_consideration = fields.Text(
        string="Overall Materiality Consideration",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    performance_materiality_percentage = fields.Float(
        string="Performance Materiality Percentage",
        default=0.0,
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    performance_materiality = fields.Monetary(
        string="Performance Materiality",
        compute="_compute_materiality",
        store=True,
        currency_field="currency_id",
    )
    performance_materiality_extrapolation = fields.Monetary(
        string="Extrapolation Performance Materiality",
        compute="_compute_materiality",
        store=True,
        currency_field="currency_id",
    )
    performance_materiality_consideration = fields.Text(
        string="Performence Materiality Consideration",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    tolerable_misstatement_percentage = fields.Float(
        string="Tolerable Misstatement Percentage",
        default=0.0,
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    tolerable_misstatement = fields.Monetary(
        string="Tolerable Misstatement",
        compute="_compute_materiality",
        store=True,
        currency_field="currency_id",
    )
    tolerable_misstatement_extrapolation = fields.Monetary(
        string="Extrapolation Tolerable Misstatement",
        compute="_compute_materiality",
        store=True,
        currency_field="currency_id",
    )
    tolerable_misstatement_consideration = fields.Text(
        string="Tolerable Misstatement Consideration",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
