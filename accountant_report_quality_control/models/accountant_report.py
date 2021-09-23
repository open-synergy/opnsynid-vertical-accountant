# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class AccountantReport(models.Model):
    _inherit = "accountant.report"

    @api.multi
    @api.depends(
        "qc_question_ids",
        "qc_question_ids.success",
    )
    def _compute_qc_result(self):
        for report in self:
            result = True
            if report.qc_question_ids:
                qc = report.qc_question_ids.filtered(lambda r: not r.success)
                if len(qc) > 0:
                    result = False
            report.qc_pass = result

    qc_pass = fields.Boolean(
        string="QC Passed?",
        compute="_compute_qc_result",
        store=True,
    )
    qc_question_ids = fields.One2many(
        string="Questions",
        comodel_name="accountant.report_qc_question",
        inverse_name="accountant_report_id",
        copy=False,
        readonly=True,
        states={
            "confirm": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def _remove_qc_question(self):
        self.ensure_one()
        self.qc_question_ids.unlink()

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        _super = super(AccountantReport, self)
        result = _super._prepare_confirm_data()
        result.update({"qc_question_ids": self.service_id._prepare_qc_question()})
        return result

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        _super = super(AccountantReport, self)
        self._remove_qc_question()
        return _super._prepare_restart_data()

    @api.constrains("qc_pass", "state")
    def _check_qc_pass(self):
        if self.state == "finalize" and not self.qc_pass:
            warning_msg = _("Report does not pass qc check")
            raise UserError(warning_msg)
