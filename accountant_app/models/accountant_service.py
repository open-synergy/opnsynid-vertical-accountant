# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantService(models.Model):
    _name = "accountant.service"
    _inherits = {"product.product": "product_id"}
    _description = "Accountant Service"

    @api.model
    def _default_type(self):
        return "service"

    product_id = fields.Many2one(
        string="Product Link",
        comodel_name="product.product",
        required=True,
        ondelete="cascade",
    )
    assurance = fields.Boolean(
        string="Assurance Service?",
    )
