# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantGeneralAuditWorksheetType(models.Model):
    _name = "accountant.general_audit_worksheet_type"
    _description = "General Audit Worksheet Type"
    _order = "category_id, sequence, code"

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
    parent_id = fields.Many2one(
        string="Parent Worksheet",
        comodel_name="accountant.general_audit_worksheet_type",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="accountant.general_audit_worksheet_type_category",
    )
    max_number_allowed = fields.Integer(
        string="Max. Number Allowed Per Audit",
        required=True,
        default=1,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
    )
    model_id = fields.Many2one(
        string="Model",
        comodel_name="ir.model",
    )
    model = fields.Char(
        string="Model Technical Name",
        related="model_id.model",
    )

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
        res = super(AccountantGeneralAuditWorksheetType, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        args = list(args or [])
        if name:
            criteria = ["|", ("code", operator, name), ("name", operator, name)]
            criteria = criteria + args
            results = self.search(criteria, limit=limit)
            if results:
                return results.name_get()
        return res
