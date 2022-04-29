# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class AccountantClientAccount(models.Model):
    _name = "accountant.client_account"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Client Account"
    _order = "partner_id, sequence, code"

    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    partner_id = fields.Many2one(
        string="Client",
        comodel_name="res.partner",
        domain=[
            ("is_company", "=", True),
            ("parent_id", "=", False),
        ],
        required=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="accountant.client_account_type",
        required=True,
        ondelete="restrict",
    )
    normal_balance = fields.Selection(
        string="Normal Balance",
        selection=[
            ("dr", "Debit"),
            ("cr", "Credit"),
        ],
        required=True,
        default=False,
    )

    @api.onchange(
        "type_id",
    )
    def onchange_normal_balance(self):
        self.normal_balance = False
        if self.type_id:
            self.normal_balance = self.type_id.normal_balance
