# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA1504RlevantRegulationAccount(models.Model):
    _name = "ws_ra1504.relevant_regulation_account"
    _description = "RA.150.3 Relevant Regulation Related Account"
    _order = "worksheet_relevant_regulation_id, sequence"

    worksheet_relevant_regulation_id = fields.Many2one(
        string="Relevant Regulation",
        comodel_name="ws_ra1504.relevant_regulation",
        required=True,
        ondelete="cascade",
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        related="worksheet_relevant_regulation_id.worksheet_id.general_audit_id",
    )
    standard_detail_id = fields.Many2one(
        string="Standard Account",
        comodel_name="accountant.general_audit_standard_detail",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    effect_to_entity = fields.Selection(
        string="Effect to Entity",
        selection=[
            ("significant", "Significant"),
            ("no", "Not Significant"),
        ],
        default="significant",
        required=True,
    )
