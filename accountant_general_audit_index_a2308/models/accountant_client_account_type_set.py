# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAccountTypeSet(models.Model):
    _name = "accountant.client_account_type_set"
    _inherit = "accountant.client_account_type_set"

    index_a2308_sequence_id = fields.Many2one(
        string="Index A.230.8 Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
