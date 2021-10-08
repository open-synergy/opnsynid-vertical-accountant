# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantGeneralAuditMainCompetitor(models.Model):
    _name = "accountant.general_audit_main_competitor"
    _description = "Accountant General Audit Main Competitor"

    index_a2303_id = fields.Many2one(
        string="Index A.230.3",
        comodel_name="accountant.general_audit_index_a2303",
        ondelete="cascade",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        # related="general_audit_id.partner_id",
        required=True,
        ondelete="restrict",
    )
    size_relative = fields.Float(
        string="Size Relative",
        required=True,
    )
