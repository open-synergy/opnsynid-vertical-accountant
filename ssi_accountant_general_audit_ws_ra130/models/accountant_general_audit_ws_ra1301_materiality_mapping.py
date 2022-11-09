# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantGeneralAuditWS1301MaterialityMapping(models.Model):
    _name = "accountant.general_audit_ws_ra1301_materiality_mapping"
    _description = "General Audit WS RA.130.1 Materiality Mapping"
    _order = "sequence, worksheet_id, id"

    @api.depends(
        "balance",
        "extrapolation_balance",
        "worksheet_id.materiality_type",
        "use_specific_materiality",
        "specific_materiality",
        "worksheet_id.worksheet_ra130_id.overall_materiality",
        "worksheet_id.worksheet_ra130_id.overall_materiality_extrapolation",
        "worksheet_id.worksheet_ra130_id.performance_materiality",
        "worksheet_id.worksheet_ra130_id.performance_materiality_extrapolation",
    )
    def _compute_materiality(self):
        for document in self:
            materiality = materiality_extrapolation = "im"
            base = base_extrapolation = 0.0
            worksheet = document.worksheet_id

            if worksheet.worksheet_ra130_id:
                worksheet_ra130 = worksheet.worksheet_ra130_id
                if worksheet.materiality_type == "om":
                    base = worksheet_ra130.overall_materiality
                    base_extrapolation = (
                        worksheet_ra130.overall_materiality_extrapolation
                    )
                else:
                    base = worksheet_ra130.performance_materiality
                    base_extrapolation = (
                        worksheet_ra130.performance_materiality_extrapolation
                    )

                if document.balance > base:
                    materiality = "m"

                if document.extrapolation_balance > base_extrapolation:
                    materiality_extrapolation = "m"

                document.materiality = materiality
                document.materiality_extrapolation = materiality_extrapolation

                if document.use_specific_materiality:
                    specific_materiality = document.specific_materiality
                    base = (specific_materiality / 100.0) * base
                    base_extrapolation = (
                        specific_materiality / 100.0
                    ) * base_extrapolation

                if document.balance > base:
                    materiality = "m"

                if document.extrapolation_balance > base_extrapolation:
                    materiality_extrapolation = "m"

            document.final_materiality = materiality
            document.final_materiality_extrapolation = materiality_extrapolation

    worksheet_id = fields.Many2one(
        string="# RA.130.1",
        comodel_name="accountant.general_audit_ws_ra1301",
        required=True,
        ondelete="cascade",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Detail",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="standard_detail_id.currency_id",
        store=True,
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
    balance = fields.Monetary(
        string="Balance",
        related="standard_detail_id.home_statement_balance",
        store=True,
        currency_field="currency_id",
    )
    extrapolation_balance = fields.Monetary(
        string="Extrapolation Balance",
        related="standard_detail_id.extrapolation_balance",
        store=True,
        currency_field="currency_id",
    )
    materiality = fields.Selection(
        string="Materiality",
        selection=[("m", "Material"), ("im", "Immaterial")],
        compute="_compute_materiality",
        store=True,
    )
    materiality_extrapolation = fields.Selection(
        string="Materiality (Extrapolation)",
        selection=[("m", "Material"), ("im", "Immaterial")],
        compute="_compute_materiality",
        store=True,
    )
    use_specific_materiality = fields.Boolean(
        string="Use Specific Materiality",
        default=False,
    )
    specific_materiality = fields.Monetary(
        string="Specific Materiality",
        required=True,
        default=0.0,
        currency_field="currency_id",
    )
    final_materiality = fields.Selection(
        string="Final Materiality",
        selection=[("m", "Material"), ("im", "Immaterial")],
        compute="_compute_materiality",
        store=True,
    )
    final_materiality_extrapolation = fields.Selection(
        string="Final Materiality (Extrapolation)",
        selection=[("m", "Material"), ("im", "Immaterial")],
        compute="_compute_materiality",
        store=True,
    )
