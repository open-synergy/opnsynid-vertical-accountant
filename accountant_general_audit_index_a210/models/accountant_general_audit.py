# -*- coding: utf-8 -*-
# Copyright 2021 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountantGeneralAudit(models.Model):
    _name = "accountant.general_audit"
    _inherit = "accountant.general_audit"

    @api.multi
    @api.depends(
        "index_a210_ids",
    )
    def _compute_index_a210_id(self):
        for document in self:
            document.index_a210_id = False
            if len(document.index_a210_ids) > 0:
                document.index_a210_id = document.index_a210_ids[0]

    index_a210_ids = fields.Many2many(
        string="Trial Balance",
        comodel_name="accountant.general_audit_index_a210",
        relation="rel_general_audit_2_index_a210",
        column1="general_audit_id",
        column2="index_a210_id",
    )
    index_a210_id = fields.Many2one(
        string="# Index A.210",
        comodel_name="accountant.general_audit_index_a210",
        compute="_compute_index_a210_id",
        store=True,
    )
