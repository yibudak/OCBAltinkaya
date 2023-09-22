# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    weight = fields.Float(compute='_cal_move_weight', digits=dp.get_precision('Stock Weight'), store=True, compute_sudo=True)

    @api.depends("product_id", "product_uom_qty", "product_uom")
    def _cal_move_weight(self):
        for move in self.filtered(lambda moves: moves.product_id.weight > 0.00):
            picking_weight_uom = (
                move.picking_id.weight_uom_id
                or self.env[
                    "product.template"
                ]._get_weight_uom_id_from_ir_config_parameter()
            )
            weight = move.product_id.weight_uom_id._compute_quantity(
                qty=move.product_qty * move.product_id.weight,
                to_unit=picking_weight_uom,
                round=False,
            )
            move.weight = weight

    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        vals['carrier_id'] = self.sale_line_id.order_id.carrier_id.id
        return vals
