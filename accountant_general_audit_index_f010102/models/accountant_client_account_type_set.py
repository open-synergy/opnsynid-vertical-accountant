# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAccountTypeSet(models.Model):
    _inherit = "accountant.client_account_type_set"

    index_f010102_sequence_id = fields.Many2one(
        string="Index F.01.01.02 Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )