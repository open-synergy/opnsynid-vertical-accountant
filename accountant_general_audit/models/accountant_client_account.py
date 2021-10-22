# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantClientAccount(models.Model):
    _name = "accountant.client_account"
    _description = "Accountant Client Account"
    _order = "partner_id, sequence, code"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
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
    description = fields.Text(
        string="Description",
    )

    @api.onchange(
        "type_id",
    )
    def onchange_normal_balance(self):
        self.normal_balance = False
        if self.type_id:
            self.normal_balance = self.type_id.normal_balance

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            if rec.code:
                name = "[{}] {}".format(rec.code, rec.name)
            else:
                name = "%s" % (rec.name)
            result.append((rec.id, name))
        return result

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        res = super(AccountantClientAccount, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        args = list(args or [])
        if name:
            criteria = ["|", ("code", operator, name), ("name", operator, name)]
            criteria = criteria + args
            account_ids = self.search(criteria, limit=limit)
            if account_ids:
                return account_ids.name_get()
        return res
