# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountantReport(models.Model):
    _inherit = "accountant.report"

    primary_creditor_id = fields.Many2one(
        string="Primary Creditor",
        comodel_name="res.partner",
        related="partner_id.primary_creditor_id",
        store=True,
        readonly=True,
    )
