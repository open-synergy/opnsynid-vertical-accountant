# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models


class AccountantClientMaterialityAnalysisDetail(models.Model):
    _name = "accountant.client_materiality_analysis_detail"
    _description = "Accountant Client Materiality Analysis Detail"
    _order = "sequence, materiality_analysis_id, id"

    @api.multi
    @api.depends(
        "materiality_analysis_id.materiality_type",
        "materiality_analysis_id.performance_materiality",
        "materiality_analysis_id.overall_materiality",
        "extrapolation_balance",
        "specific_materiality",
        "specific_overall_materiality_percentage",
        "specific_performance_materiality_percentage",
        )
    def _compute_materiality(self):
        for document in self:
            if document.materiality_analysis_id.materiality_type == "om":
                if document.extrapolation_balance >= \
                        document.materiality_analysis_id.overall_materiality:
                    document.computed_materiality = "m"
                    document.final_materiality = "m"
                else:
                    document.computed_materiality == "nm"
                    if document.specific_materiality:
                        document.final_materiality = "m"
                        document.specific_overal_materiality = \
                          document.specific_overal_materiality * \
                          document.material_analysis_id.overal_materiality
                    else:
                        document.final_materiality = "nm"
            if document.materiality_analysis_id.materiality_type == "pm":
                if document.extrapolation_balance >= \
                    document.materiality_analysis_id.performance_materiality:
                    document.computed_materiality = "m"
                    document.final_materiality = "m"
                else:
                    document.computed_materiality = "nm"
                    if document.specific_materiality:
                        document.final_materiality = "m"
                        document.specific_overal_materiality = \
                          document.specific_overal_materiality * \
                          document.material_analysis_id.overal_materiality
                    else:
                        document.final_materiality = "nm"

    materiality_analysis_id = fields.Many2one(
        string="Materiality Analysis",
        comodel_name="accountant.client_materiality_analysis",
        required=True,
        ondelete="cascade",
    )
    detail_id = fields.Many2one(
        string="Detail",
        comodel_name="accountant.client_trial_balance_standard_detail",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        readonly=True,
        store=True,
        related="detail_id.sequence",
    )
    code = fields.Char(
        string="Code",
        readonly=True,
        related="detail_id.type_id.code",
    )
    name = fields.Char(
        string="Name",
        readonly=True,
        related="detail_id.type_id.name",
    )
    previous_balance = fields.Float(
        string="Previous Balance",
        readonly=True,
        related="detail_id.previous_balance",
    )
    balance = fields.Float(
        string="Balance",
        readonly=True,
        related="detail_id.balance",
    )
    extrapolation_balance = fields.Float(
        string="Balance",
        readonly=True,
        related="detail_id.extrapolation_balance",
    )

    specific_materiality = fields.Boolean(
        string="Specific Materiality",
        default=False,
    )
    computed_materiality = fields.Selection(
        string="Compute Materiality",
        selection=[
            ("m", "Material"),
            ("n", "Non Material"),
        ],
        compute="_compute_materiality",
        store=True,
    )
    final_materiality = fields.Selection(
        string="Final Materiality",
        selection=[
            ("m", "Material"),
            ("n", "Non Material"),
        ],
        compute="_compute_materiality",
        store=True,
    )
    specific_overall_materiality_percentage = fields.Float(
        string="Specific Overall Materiality Percentage",
    )
    specific_overall_materiality = fields.Float(
        string="Specific Overall Materiality",
        compute="_compute_materiality",
        store=True,
    )
    specific_performance_materiality_percentage = fields.Float(
        string="Specific Performance Materiality Percentage",
    )
    specific_performance_materiality = fields.Float(
        string="Specific Performance Materiality",
        compute="_compute_materiality",
        store=True,
    )
