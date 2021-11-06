# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantRelevantExternalFactor(models.Model):
    _name = "accountant.relevant_external_factor"
    _description = "External Factor"
    _order = "sequence, id"

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
    description = fields.Text(
        string="Description",
    )
    effective_date = fields.Date(
        string="Effective Date",
        required=True,
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="accountant.relevant_external_factor_category",
        ondelete="restrict",
        required=True,
    )
