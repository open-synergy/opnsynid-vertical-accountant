# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AccountantClientAccountType(models.Model):
    _name = "accountant.client_account_type"
    _inherit = "accountant.client_account_type"

    compute_diff = fields.Boolean(
        string="Compute Diff.",
        default=True,
    )
