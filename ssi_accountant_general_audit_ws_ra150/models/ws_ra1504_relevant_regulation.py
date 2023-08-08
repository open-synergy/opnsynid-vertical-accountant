# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class WSAuditRA1504RlevantRegulation(models.Model):
    _name = "ws_ra1504.relevant_regulation"
    _description = "RA.150.3 Relevant Regulation"
    _order = "worksheet_id, sequence"

    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="ws_ra1504",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    relevant_regulation_id = fields.Many2one(
        string="Relevant Regulation",
        comodel_name="accountant.relevant_regulation",
        ondelete="restrict",
    )
    relevant_regulation = fields.Char(
        string="Regulation Name/Number",
        required=True,
    )
    detail_regulation = fields.Char(
        string="Relevant Content",
        required=True,
    )
    account_ids = fields.One2many(
        string="Related Account",
        comodel_name="ws_ra1504.relevant_regulation_account",
        inverse_name="worksheet_relevant_regulation_id",
    )

    @api.onchange(
        "relevant_regulation_id",
    )
    def onchange_relevant_regulation(self):
        self.relevant_regulation = False
        if self.relevant_regulation_id:
            self.relevant_regulation = self.relevant_regulation_id.name
