# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class WSAuditRA1402(models.Model):
    _name = "ws_ra1402"
    _description = "General Audit WS RA.140.2"
    _inherit = [
        "accountant.general_audit_worksheet_mixin",
    ]
    _type_xml_id = "ssi_accountant_general_audit_ws_ra140.worksheet_type_ra1402"

    ratio_ids = fields.One2many(
        string="Ratio Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
    )
    liquidity_ratio_ids = fields.One2many(
        string="Liquidity Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("financial_ratio_id.category", "=", "liquidity"),
        ],
    )
    activity_ratio_ids = fields.One2many(
        string="Activity Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("financial_ratio_id.category", "=", "activity"),
        ],
    )
    solvency_ratio_ids = fields.One2many(
        string="Solvency Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("financial_ratio_id.category", "=", "solvency"),
        ],
    )
    profitability_ratio_ids = fields.One2many(
        string="Profitability Ratio",
        comodel_name="ws_ra1402.ratio",
        inverse_name="worksheet_id",
        domain=[
            ("financial_ratio_id.category", "=", "profitability"),
        ],
    )

    @api.onchange("general_audit_id")
    def onchange_ratio_ids(self):
        self.update({"ratio_ids": [(5, 0, 0)]})
        FinancialRatio = self.env["accountant.financial_ratio"]
        if self.general_audit_id:
            result = []
            for ratio in FinancialRatio.search([]):
                result.append(
                    (
                        0,
                        0,
                        {
                            "financial_ratio_id": ratio.id,
                        },
                    )
                )
            self.update({"ratio_ids": result})

    def action_compute_ratio(self):
        for record in self:
            record._recompute_computation()

    @ssi_decorator.post_confirm_action()
    def _recompute_computation(self):
        self.ensure_one()
        additional_dict = self._get_additional_dict()
        for computation in self.ratio_ids:
            additionaldict = computation._recompute(additional_dict)
            additional_dict = additionaldict

        self.general_audit_id._recompute_extrapolation_computation()

    def _get_additional_dict(self):
        self.ensure_one()
        result = {"account_type": {}, "account_group": {}, "computation": {}}
        # Load general audit's standard detail to dict
        for data in self.general_audit_id.standard_detail_ids:
            result["account_type"].update(
                {
                    data.type_id.code: {
                        "extrapolation": data.extrapolation_balance,
                        "interim": data.interim_balance,
                        "previous": data.previous_balance,
                        "extrapolation_avg": data.extrapolation_avg,
                        "interim_avg": data.interim_avg,
                    },
                }
            )

        # Load general audit's group summary to dict
        for data in self.general_audit_id.group_detail_ids:
            result["account_group"].update(
                {
                    data.group_id.code: {
                        "extrapolation": data.extrapolation_balance,
                        "interim": data.interim_balance,
                        "previous": data.previous_balance,
                        "extrapolation_avg": data.extrapolation_avg,
                        "interim_avg": data.interim_avg,
                    },
                }
            )

        # Load general audit's computation to dict
        for data in self.general_audit_id.computation_ids:
            result["computation"].update(
                {
                    data.computation_item_id.code: {
                        "extrapolation": data.extrapolation_amount,
                        "interim": data.interim_amount,
                        "previous": data.previous_amount,
                        "extrapolation_avg": data.extrapolation_avg_amount,
                        "interim_avg": data.interim_avg_amount,
                    },
                }
            )
        return result
