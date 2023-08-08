# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AccountantGeneralAuditWorksheetTypeCategory(models.Model):
    _name = "accountant.general_audit_worksheet_type_category"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit Worksheet Type Category"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
