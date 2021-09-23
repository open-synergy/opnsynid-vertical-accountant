# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class ConvertProductToService(models.TransientModel):
    _name = "accountant.convert_product_to_service"
    _description = "Convert Product To Accountant Service"

    @api.model
    def _default_product_ids(self):
        result = []

        if self._context.get("active_model", False) != "product.product":
            return result

        product_ids = self._context.get("active_ids", [])
        return [(6, 0, product_ids)]

    product_ids = fields.Many2many(
        string="Product to Convert",
        comodel_name="product.product",
        relation="rel_convert_product_to_accountant_service",
        column1="wizard_id",
        column2="product_id",
        default=lambda self: self._default_product_ids(),
    )

    @api.multi
    def action_convert(self):
        self.ensure_one()
        obj_service = self.env["accountant.service"]
        for product in self.product_ids:
            if not self._check_product(product):
                raise UserError(_("Service already exist"))
            obj_service.create(self._prepare_service_data(product))

    @api.model
    def _check_product(self, product):
        obj_service = self.env["accountant.service"]
        criteria = [
            ("product_id", "=", product.id),
        ]
        return True if obj_service.search_count(criteria) == 0 else False

    @api.model
    def _prepare_service_data(self, product):
        return {
            "product_id": product.id,
        }
