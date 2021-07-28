# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountantClientAccountTypeSet(models.Model):
    _inherit = "accountant.client_account_type_set"

    accountant_general_audit_index_a1102_sequence_id = fields.Many2one(
        string="Accountant General Audit Index 1102 Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
