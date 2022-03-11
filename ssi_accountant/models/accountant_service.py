# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountantService(models.Model):
    _name = "accountant.service"
    _description = "Accountant Service"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        ondelete="restrict",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
    )
