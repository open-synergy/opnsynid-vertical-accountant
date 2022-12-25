# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

import base64
import csv
import io

from odoo import api, fields, models


class ImportClientAccount(models.TransientModel):
    _name = "import_client_account"
    _description = "Import Trial Balance Detail"

    @api.model
    def _default_general_audit_id(self):
        return self.env.context.get("active_id", False)

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="accountant.general_audit",
        default=lambda self: self._default_general_audit_id(),
    )
    data = fields.Binary(string="File", required=True)

    def button_import(self):
        self.ensure_one()
        csv_data = base64.b64decode(self.data)
        data_file = io.StringIO(csv_data.decode("utf-8"))
        data_file.seek(0)
        reader = csv.reader(data_file, delimiter=",")
        for row in reader:
            self._import_client_account(row)
        self.general_audit_id.action_reload_account()
        return {"type": "ir.actions.act_window_close"}

    def _import_client_account(self, row):
        self.ensure_one()
        Account = self.env["accountant.client_account"]
        criteria = [
            ("partner_id", "=", self.general_audit_id.partner_id.id),
            ("code", "=", row[0]),
        ]
        count = Account.search_count(criteria)
        if count > 0:
            return True
        Account.create(
            {
                "code": row[0],
                "name": row[1],
                "partner_id": self.general_audit_id.partner_id.id,
            }
        )
