# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import csv
from tempfile import TemporaryFile

from openerp import api, fields, models


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

    @api.multi
    def button_import(self):
        self.ensure_one()
        fileobj = TemporaryFile("w+")
        fileobj.write(base64.decodestring(self.data))
        fileobj.seek(0)
        reader = csv.reader(fileobj, delimiter=",")
        self.trial_balance_id.detail_ids.unlink()
        for row in reader:
            self._create_trial_balance_detail(row)

        fileobj.close()
        return {"type": "ir.actions.act_window_close"}

    @api.multi
    def _create_trial_balance_detail(self, row):
        self.ensure_one()
        obj_detail = self.env["accountant.client_trial_balance_detail"]
        obj_detail.create(self._prepare_trial_balance_detail(row))

    @api.multi
    def _prepare_trial_balance_detail(self, row):
        self.ensure_one()
        obj_type = self.env["accountant.client_account_type"]
        criteria = [("name", "=", row[2])]
        account_type = obj_type.search(criteria)[0]
        return {
            "trial_balance_id": self.trial_balance_id.id,
            "code": row[1],
            "name": row[0],
            "type_id": account_type.id,
            "sequence": account_type.sequence,
            "balance": row[3],
            "interim_balance": row[4],
            "previous_balance": row[5],
        }
