import random
import string
from odoo import models, fields, api

class StockIn(models.Model):
    _name = 'nhom8.stock.in'
    _description = 'Phiếu nhập kho'

    stock_in_id = fields.Char(string="Mã phiếu nhập", required=True, copy=False, readonly=True, default='PN', index=True, unique=True)
    date_in = fields.Datetime(string="Ngày nhập", default=fields.Datetime.now, required=True)
    supplier = fields.Char(string="Nhà cung cấp")
    line_ids = fields.One2many('nhom8.stock.in.line', 'stock_in_id', string="Chi tiết phiếu nhập")
    total_price = fields.Float(string="Tổng tiền", compute="_compute_total_price", store=True)

    @api.depends('line_ids.total_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(line.total_price for line in record.line_ids)

    @api.model
    def create(self, vals):
        if 'stock_in_id' not in vals or vals['stock_in_id'] == 'PN':
            vals['stock_in_id'] = self.generate_unique_stock_in_id()

        stock_in_record = super(StockIn, self).create(vals)

        for line in stock_in_record.line_ids:
            line.update_product_inventory()

        return stock_in_record

    def generate_unique_stock_in_id(self):
        while True:
            new_id = 'PN-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not self.search([('stock_in_id', '=', new_id)]):
                return new_id
    def action_cancel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Danh sách Phiếu Nhập',
            'res_model': 'nhom8.stock.in',
            'view_mode': 'tree,form',
            'target': 'current',
        }