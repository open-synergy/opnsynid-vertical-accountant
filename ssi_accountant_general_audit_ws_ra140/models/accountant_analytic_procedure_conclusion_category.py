# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AccountantAnalyticProcedureConsulsionCategory(models.Model):
    _name = "accountant.analytic_procedure_conclusion_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Analytic Procedure Consulsion Category"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    parent_id = fields.Many2one(
        string="Parent",
        comodel_name="accountant.analytic_procedure_conclusion_category",
    )
