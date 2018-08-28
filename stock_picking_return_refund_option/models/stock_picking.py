# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    to_refund_lines = fields.Selection(selection=[
        ('keep_line_value', 'Keep Line Value'),
        ('to_refund', 'To Refund'),
        ('no_refund', 'No Refund')],
        string='Refund Options', default='keep_line_value',
        help="This field allow modify 'to_refund' field value in all "
             "stock moves from this picking after it has been confirmed."
             "keep_line_value: keep the original value.\n"
             "to_refund: set all stock moves to True value and recompute "
             "delivered quantities in sale order.\n"
             "no_refund: set all stock moves to False value and recompute "
             "delivered quantities in sale/purchase order.",
    )
    is_return = fields.Boolean(compute='_compute_is_return')

    def _compute_is_return(self):
        for picking in self:
            if any(x.origin_returned_move_id for x in picking.move_lines):
                picking.is_return = True

    @api.multi
    def _update_stock_moves(self):
        for pick in self.filtered(
                lambda x: x.to_refund_lines != 'keep_line_value'):
            pick.move_lines.write({
                'to_refund': pick.to_refund_lines == 'to_refund',
            })
        for move in self.filtered(
                lambda x: x.to_refund_lines == 'keep_line_value'
                ).mapped('move_lines'):
            move.to_refund = move.origin_to_refund

    @api.multi
    def set_delivered_qty(self):
        if hasattr(self.env['stock.move'], 'sale_line_id') and self.sale_id:
            # The sale_stock module is installed
            so_lines = self.mapped('move_lines.sale_line_id').filtered(
                lambda x: x.product_id.invoice_policy in ('order', 'delivery'))
            for so_line in so_lines:
                so_line.qty_delivered = so_line._get_delivered_qty()

    @api.multi
    def set_received_qty(self):
        if (hasattr(self.env['stock.move'], 'purchase_line_id') and
                self.purchase_id):
            # The purchase module is installed
            po_lines = self.mapped('move_lines.purchase_line_id').filtered(
                lambda x: x.product_id.invoice_policy in ('order', 'delivery'))
            po_lines._compute_qty_received()

    @api.multi
    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        if 'to_refund_lines' in vals:
            for picking in self:
                picking._update_stock_moves()
                picking.set_delivered_qty()
                picking.set_received_qty()
        return res
