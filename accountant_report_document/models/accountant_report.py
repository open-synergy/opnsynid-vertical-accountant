# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountantReport(models.Model):
    _inherit = "accountant.report"

    attachment_ids = fields.One2many(
        string="Attachments",
        comodel_name="ir.attachment",
        inverse_name="res_id",
        domain=[
            ("res_model", "=", "accountant.report"),
        ],
        auto_join=True,
    )
