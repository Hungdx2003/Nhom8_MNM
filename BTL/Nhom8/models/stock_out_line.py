from odoo import models, fields, api

class StockOutLine(models.Model):
    _name = 'nhom8.stock.out.line'
    _description = 'Chi tiết phiếu xuất'

    stock_out_id = fields.Many2one('nhom8.stock.out', string="Mã phiếu xuất", required=True, ondelete="cascade")
    product_id = fields.Many2one('nhom8.product', string="Sản phẩm", required=True)
    quantity = fields.Float(string="Số lượng", required=True)
    sale_price = fields.Float(string="Giá bán", compute="_compute_sale_price", store=True)
    total_price = fields.Float(string="Thành tiền", compute="_compute_total_price", store=True)

    @api.depends('quantity', 'sale_price')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.quantity * line.sale_price

    @api.depends('product_id')
    def _compute_sale_price(self):
        """Cập nhật giá bán dựa trên giá xuất trong bảng sản phẩm khi chọn sản phẩm"""
        for line in self:
            line.sale_price = line.product_id.sale_price if line.product_id else 0

    def update_inventory(self):
        """Giảm số lượng tồn kho sau khi xuất sản phẩm"""
        inventory_record = self.env['nhom8.inventory'].search([('product_id', '=', self.product_id.id)], limit=1)
        
        if inventory_record:
            if inventory_record.quantity >= self.quantity:
                # Giảm số lượng trong tồn kho
                inventory_record.quantity -= self.quantity
                inventory_record.last_updated = fields.Datetime.now()
            else:
                # Thông báo lỗi nếu không đủ tồn kho
                raise ValueError(f"Sản phẩm {self.product_id.name} không đủ tồn kho. Tồn kho hiện tại: {inventory_record.quantity}.")
        else:
            # Báo lỗi nếu sản phẩm không tồn tại trong tồn kho
            raise ValueError(f"Sản phẩm {self.product_id.name} không có trong tồn kho.")
