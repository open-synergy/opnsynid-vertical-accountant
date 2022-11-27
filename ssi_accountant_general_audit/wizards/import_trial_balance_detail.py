# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

import base64
import csv
import io

from odoo import api, fields, models


class ImportTrialBalanceDetail(models.TransientModel):
    _name = "accountant.import_trial_balance_detail"
    _description = "Import Trial Balance Detail"

    @api.model
    def _default_trial_balance_id(self):
        return self.env.context.get("active_id", False)

    trial_balance_id = fields.Many2one(
        string="# Trial Balance",
        comodel_name="accountant.client_trial_balance",
        default=lambda self: self._default_trial_balance_id(),
        store=True,
        compute=False,
    )
    data = fields.Binary(string="File", required=True)

    def button_import(self):
        self.ensure_one()
        csv_data = base64.b64decode(self.data)
        data_file = io.StringIO(csv_data.decode("utf-8"))
        data_file.seek(0)
        reader = csv.reader(data_file, delimiter=",")
        for row in reader:
            self._update_trial_balance_detail(row)
        return {"type": "ir.actions.act_window_close"}

    def _update_trial_balance_detail(self, row):
        self.ensure_one()
        Detail = self.env["accountant.client_trial_balance_detail"]
        criteria = [
            ("trial_balance_id", "=", self.trial_balance_id.id),
            ("account_id.code", "=", row[0]),
        ]
        Detail.search(criteria).write(
            {
                "opening_balance_debit": row[2],
                "opening_balance_credit": row[3],
                "debit": row[4],
                "credit": row[5],
            }
        )
