# -*- coding: utf-8 -*-
# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantGeneralAuditIndexA2101Detail(models.Model):
    _name = "accountant.general_audit_index_a2101_detail"
    _description = "Accountant General Audit Index A.210.1 Details"
    _order = "sequence, index_a2101_id, id"

    @api.multi
    @api.depends(
        "balance",
        "extrapolation_balance",
        "index_a2101_id.materiality_type",
        "use_specific_materiality",
        "specific_materiality",
        "index_a2101_id.general_audit_id.index_a210_id.overall_materiality",
        "index_a2101_id.general_audit_id.index_a210_id."
        "overall_materiality_extrapolation",
        "index_a2101_id.general_audit_id.index_a210_id.performance_materiality",
        "index_a2101_id.general_audit_id.index_a210_id."
        "performance_materiality_extrapolation",
    )
    def _compute_significancy(self):
        for document in self:
            significancy = significancy_extrapolation = "ns"
            base = base_extrapolation = 0.0
            index_a2101 = document.index_a2101_id
            if index_a2101.general_audit_id.index_a210_id:
                index_a210 = index_a2101.general_audit_id.index_a210_id
                if index_a2101.materiality_type == "om":
                    base = index_a210.overall_materiality
                    base_extrapolation = index_a210.overall_materiality_extrapolation
                else:
                    base = index_a210.performance_materiality
                    base_extrapolation = (
                        index_a210.performance_materiality_extrapolation
                    )

                if document.balance > base:
                    significancy = "s"

                if document.extrapolation_balance > base_extrapolation:
                    significancy_extrapolation = "s"

                document.significancy = significancy
                document.significancy_extrapolation = significancy_extrapolation

                if document.use_specific_materiality:
                    specific_materiality = document.specific_materiality
                    base = (specific_materiality / 100.0) * base
                    base_extrapolation = (
                        specific_materiality / 100.0
                    ) * base_extrapolation

                if document.balance > base:
                    significancy = "s"

                if document.extrapolation_balance > base_extrapolation:
                    significancy_extrapolation = "s"

                document.final_significancy = significancy
                document.final_significancy_extrapolation = significancy_extrapolation

    index_a2101_id = fields.Many2one(
        string="# Index A.201.1",
        comodel_name="accountant.general_audit_index_a2101",
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
        string="Balance",
        related="standard_detail_id.extrapolation_balance",
        store=True,
    )
    significancy = fields.Selection(
        string="Significancy",
        selection=[("s", "Significant"), ("ns", "Not Significant")],
        compute="_compute_significancy",
        store=True,
    )
    significancy_extrapolation = fields.Selection(
        string="Significancy (Extrapolation)",
        selection=[("s", "Significant"), ("ns", "Not Significant")],
        compute="_compute_significancy",
        store=True,
    )
    use_specific_materiality = fields.Boolean(
        string="Use Specific Materiality",
        default=False,
    )
    specific_materiality = fields.Float(
        string="Specific Materiality",
        required=True,
        default=0.0,
    )
    final_significancy = fields.Selection(
        string="Final Significancy",
        selection=[("s", "Significant"), ("ns", "Not Significant")],
        compute="_compute_significancy",
        store=True,
    )
    final_significancy_extrapolation = fields.Selection(
        string="Final Significancy (Extrapolation)",
        selection=[("s", "Significant"), ("ns", "Not Significant")],
        compute="_compute_significancy",
        store=True,
    )
