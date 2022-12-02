# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA1503BusinessProcess(models.Model):
    _name = "ws_ra1503.business_process"
    _description = "RA.150.3 Business Process"
    _order = "worksheet_id, sequence"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra1503",
        required=True,
        ondelete="cascade",
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        related="worksheet_id.general_audit_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    business_process_id = fields.Many2one(
        string="Business Process",
        comodel_name="accountant.business_process",
        required=True,
        ondelete="restrict",
    )
    description = fields.Text(
        string="Description",
    )
