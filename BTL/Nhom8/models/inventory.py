from odoo import models, fields, api

class Inventory(models.Model):
    _name = 'nhom8.inventory'
    _description = 'Inventory Management'

    product_id = fields.Many2one('nhom8.product', string='Sản phẩm', required=True)
    quantity = fields.Integer(string='Số lượng', required=True, default=0)
    location = fields.Char(string='Địa điểm')
    last_updated = fields.Datetime(string='Cập nhật cuối', default=fields.Datetime.now)

