# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantFraudInquiryItem(models.Model):
    _name = "accountant.fraud_inquiry_item"
    _description = "Fraud Inquiry Item"
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
    description = fields.Text(
        string="Description",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="accountant.fraud_inquiry_item_category",
        ondelete="restrict",
        required=True,
    )
