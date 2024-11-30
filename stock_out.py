import random
import string
from odoo import models, fields, api

class StockOut(models.Model):
    _name = 'nhom8.stock.out'
    _description = 'Phiếu xuất kho'

    stock_out_id = fields.Char(string="Mã phiếu xuất", required=True, readonly=True, copy=False, default='PX')
    date_out = fields.Date(string="Ngày xuất", default=fields.Date.context_today, required=True)
    customer = fields.Char(string="Khách hàng")
    total_price = fields.Float(string="Tổng tiền", compute="_compute_total_price", store=True, readonly=True)
    line_ids = fields.One2many('nhom8.stock.out.line', 'stock_out_id', string="Các sản phẩm")
  
    @api.depends('line_ids.total_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(line.total_price for line in record.line_ids)

    @api.model
    def create(self, vals):
        if 'stock_out_id' not in vals or vals['stock_out_id'] == 'PX':
            vals['stock_out_id'] = self.generate_unique_stock_out_id()

        stock_out_record = super(StockOut, self).create(vals)

        for line in stock_out_record.line_ids:
            line.update_inventory()

        return stock_out_record

    def generate_unique_stock_out_id(self):
        while True:
            new_id = 'PX-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not self.search([('stock_out_id', '=', new_id)]):
                return new_id