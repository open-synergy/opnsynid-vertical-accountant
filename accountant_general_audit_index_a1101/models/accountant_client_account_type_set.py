# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAccountTypeSet(models.Model):
    _name = "accountant.client_account_type_set"
    _inherit = "accountant.client_account_type_set"

    index_a1101_sequence_id = fields.Many2one(
        string="Index A1101 Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
