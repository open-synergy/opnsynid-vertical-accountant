# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WS1201AccountMapping(models.Model):
    _name = "ws_ra1201.account_mapping"
    _description = "General Audit WS RA.120.1 Account Mapping"

    worksheet_id = fields.Many2one(
        string="# RA.120.1",
        comodel_name="ws_ra1201",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="account_id.sequence",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="accountant.client_account",
        required=True,
    )
    code = fields.Char(
        string="Code",
        related="account_id.code",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="accountant.client_account_type",
        related="account_id.type_id",
        store=True,
        readonly=False,
    )
    normal_balance = fields.Selection(
        string="Normal Balance",
        related="type_id.normal_balance",
    )
