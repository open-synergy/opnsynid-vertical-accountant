# -*- coding: utf-8 -*-
# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantGeneralAudit(models.Model):
    _name = "accountant.general_audit"
    _inherit = "accountant.general_audit"

    @api.multi
    @api.depends(
        "index_a2303_ids",
    )
    def _compute_index_a2303_id(self):
        for document in self:
            document.index_a2303_id = False
            if len(document.index_a2303_ids) > 0:
                document.index_a2303_id = document.index_a2303_ids[0]

    index_a2303_ids = fields.Many2many(
        string="Index A.230.3",
        comodel_name="accountant.general_audit_index_a2303",
        relation="rel_general_audit_2_index_a2303",
        column1="general_audit_id",
        column2="index_a2303_id",
    )
    index_a2303_id = fields.Many2one(
        string="# Index A.230.3",
        comodel_name="accountant.general_audit_index_a2303",
        compute="_compute_index_a2303_id",
        store=True,
    )
