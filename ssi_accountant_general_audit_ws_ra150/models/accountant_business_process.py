# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class AccountantBusinessProcess(models.Model):
    _name = "accountant.business_process"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant - Business Process"
