# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA2203AccountControlActivity(models.Model):
    _name = "ws_ra2203.account_control_activity"
    _description = "RA.220.3 Account Control Activity"

    account_id = fields.Many2one(
        string="Account Cycle",
        comodel_name="ws_ra2203.account_cycle",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=1,
    )
    name = fields.Char(
        string="Control Activity",
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
