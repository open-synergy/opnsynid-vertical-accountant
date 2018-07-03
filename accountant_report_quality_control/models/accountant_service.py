# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountantService(models.Model):
    _inherit = "accountant.service"

    qc_question_ids = fields.One2many(
        string="Questions",
        comodel_name="accountant.service_qc_question",
        inverse_name="accountant_service_id",
    )

    @api.multi
    def _prepare_qc_question(self):
        self.ensure_one()
        result = []
        for question in self.qc_question_ids:
            data = question._prepare_qc_question()
            result.append((0, 0, data))
        return result
