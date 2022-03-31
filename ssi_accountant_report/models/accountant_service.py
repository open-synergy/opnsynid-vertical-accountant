# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import fields, models


class AccountantService(models.Model):
    _inherit = "accountant.service"

    assurance = fields.Boolean(
        string="Assurance Service?",
    )

    allowed_opinion_ids = fields.Many2many(
        string="Allowed Opinion",
        comodel_name="accountant.report_opinion",
        relation="rel_accountant_service_2_opinion",
        column1="service_id",
        column2="opini_id",
    )
    allowed_method_ids = fields.Many2many(
        string="Allowed Methods",
        comodel_name="accountant.report_method",
        relation="rel_accountant_service_2_method",
        column1="method_id",
        column2="opini_id",
    )
    opinion_required = fields.Boolean(
        string="Opinion Required",
    )
    method_required = fields.Boolean(
        string="Method Required",
    )
