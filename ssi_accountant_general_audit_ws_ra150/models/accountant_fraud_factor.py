# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class AccountantFraudFactor(models.Model):
    _name = "accountant.fraud_factor"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Accountant - Fraud Factor"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=5,
    )
    category = fields.Selection(
        string="Category",
        selection=[
            ("preassure", "Preassure"),
            ("opportunity", "Opportunity"),
            ("rationalization", "Rationalization"),
        ],
        required=True,
    )
