# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class WSAuditRA1503Expert(models.Model):
    _name = "ws_ra1503.expert"
    _description = "RA.150.3 Expert"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra1503",
        required=True,
        ondelete="cascade",
    )
    expert_name = fields.Char(
        string="Expert Name/Institution",
        required=True,
    )
    job = fields.Char(
        string="Job",
        required=True,
    )
    documentation = fields.Char(
        string="Documentation",
    )
    standard_detail_ids = fields.Many2many(
        string="Standard Account",
        comodel_name="accountant.general_audit_standard_detail",
        relation="rel_expert_2_general_audit_standard_detail",
        column1="expert_id",
        column2="standard_detail_id",
        required=False,
    )
