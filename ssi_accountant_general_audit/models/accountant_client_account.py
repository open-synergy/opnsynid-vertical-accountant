# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountantClientAccount(models.Model):
    _name = "accountant.client_account"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Client Account"
    _order = "partner_id, sequence, code"
    _show_code_on_display_name = True

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
        required=False,
        ondelete="restrict",
    )
    normal_balance = fields.Selection(
        string="Normal Balance",
        related="type_id.normal_balance",
        stored=True,
        required=False,
    )

    @api.onchange(
        "type_id",
    )
    def onchange_normal_balance(self):
        self.normal_balance = False
        if self.type_id:
            self.normal_balance = self.type_id.normal_balance

    @api.constrains("code")
    def _check_duplicate_code(self):
        error_msg = _("Duplicate code not allowed")
        for record in self:
            criteria = [
                ("code", "=", record.code),
                ("id", "!=", record.id),
                ("partner_id", "=", record.partner_id.id),
            ]
            count_duplicate = self.search_count(criteria)
            if count_duplicate > 0:
                raise UserError(error_msg)
