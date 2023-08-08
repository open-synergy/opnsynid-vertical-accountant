# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountantService(models.Model):
    _name = "accountant.service"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant Service"

    name = fields.Char(
        string="Accountant Service",
    )
    assurance = fields.Boolean(
        string="Assurance Service?",
    )
    allowed_opinion_ids = fields.Many2many(
        string="Allowed Opinion",
        comodel_name="accountant.opinion",
        relation="rel_accountant_service_2_opinion",
        column1="service_id",
        column2="opinion_id",
    )
