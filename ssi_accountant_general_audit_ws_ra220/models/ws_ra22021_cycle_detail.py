# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA22021Cycle(models.Model):
    _name = "ws_ra22021.cycle_detail"
    _description = "RA.220.2.1 Cycle Detail"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra22021",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=1,
    )
    name = fields.Char(
        string="Cycle Item",
        required=True,
    )
    frequency = fields.Char(
        string="Frequency",
        required=True,
    )
    risk_identification = fields.Text(
        string="Risk Identification",
        required=True,
    )
    what_can_go_wrong = fields.Text(
        string="What Can Go Wrong",
        required=True,
    )
    activity_control_documentation = fields.Text(
        string="Activity Control Documentation",
        required=True,
    )
