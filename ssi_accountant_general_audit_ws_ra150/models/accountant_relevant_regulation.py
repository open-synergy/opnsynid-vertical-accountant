# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class AccountantRelevantRegulation(models.Model):
    _name = "accountant.relevant_regulation"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant - Relevant Regulation"
