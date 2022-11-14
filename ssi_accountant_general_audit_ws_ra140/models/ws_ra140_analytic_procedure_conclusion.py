# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA140AnalyticProcedureConclusion(models.Model):
    _name = "ws_ra140.analytic_procedure_conclusion"
    _description = "Analytic Procedure Consulsion Category"
    _order = "parent_sequence, sequence, id"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra140",
        required=True,
        ondelete="cascade",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="accountant.analytic_procedure_conclusion_category",
        required=True,
        ondelete="restrict",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="category_id.sequence",
        store=True,
    )
    parent_sequence = fields.Integer(
        string="Parent Sequence",
        related="category_id.parent_id.sequence",
        store=True,
    )
    name = fields.Text(
        string="Conclusion",
        required=True,
    )
