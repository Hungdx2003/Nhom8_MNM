from odoo import models, fields, api

class StockInLine(models.Model):
    _name = 'nhom8.stock.in.line'
    _description = 'Chi tiết phiếu nhập'

    stock_in_id = fields.Many2one('nhom8.stock.in', string="Mã phiếu nhập", required=True, ondelete="cascade")
    product_id = fields.Many2one('nhom8.product', string="Sản phẩm", required=True)
    quantity = fields.Float(string="Số lượng", required=True)
    purchase_price = fields.Float(string="Giá nhập", required=True)
    total_price = fields.Float(string="Thành tiền", compute="_compute_total_price", store=True)

    @api.depends('quantity', 'purchase_price')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.quantity * line.purchase_price

    def update_product_inventory(self):
        """Cập nhật giá nhập và số lượng sản phẩm trong tồn kho"""

        self.product_id.purchase_price = self.purchase_price
        
        inventory_record = self.env['nhom8.inventory'].search([('product_id', '=', self.product_id.id)], limit=1)
        
        if inventory_record:
            inventory_record.quantity += self.quantity
            inventory_record.last_updated = fields.Datetime.now()
        else:
            self.env['nhom8.inventory'].create({
                'product_id': self.product_id.id,
                'quantity': self.quantity,
                'location': 'Kho chính',
                'last_updated': fields.Datetime.now()
            })
