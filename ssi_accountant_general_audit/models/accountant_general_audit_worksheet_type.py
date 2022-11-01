# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class AccountantGeneralAuditWorksheetType(models.Model):
    _name = "accountant.general_audit_worksheet_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Worksheet Type"
    _order = "category_id, sequence, code"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    parent_id = fields.Many2one(
        string="Parent Worksheet",
        comodel_name="accountant.general_audit_worksheet_type",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="accountant.general_audit_worksheet_type_category",
    )
    max_number_allowed = fields.Integer(
        string="Max. Number Allowed Per Audit",
        required=True,
        default=1,
    )
    model_id = fields.Many2one(
        string="Model",
        comodel_name="ir.model",
    )
    model = fields.Char(
        string="Model Technical Name",
        related="model_id.model",
    )