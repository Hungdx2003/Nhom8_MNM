import random
import string
from odoo import models, fields,api

class Product(models.Model):
    _name = 'nhom8.product'
    _description = 'Danh sách sản phẩm'

    product_id = fields.Char(string="Mã Sản Phẩm", required=True, index=True, unique=True, default='SP')
    name = fields.Char(string="Tên Sản Phẩm", required=True)
    category = fields.Char(string="Loại Sản Phẩm")
    unit = fields.Char(string="Đơn Vị Tính", required=True)
    purchase_price = fields.Float(string="Giá Nhập", required=True)
    sale_price = fields.Float(string="Giá Xuất", required=True)
    description = fields.Text(string="Mô Tả")
    supplier = fields.Char(string="Nhà Cung Cấp")

    @api.model
    def create(self, vals):
        # Tạo mã sản phẩm tự động
        if 'product_id' not in vals or not vals['product_id']:
            vals['product_id'] = self.generate_product_id()

        return super(Product, self).create(vals)

    def generate_product_id(self):
        # Tạo mã sản phẩm ngẫu nhiên
        return 'SP-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def generate_unique_product_id(self):
        while True:
            # Tạo mã phiếu nhập ngẫu nhiên theo định dạng
            new_id = 'SP-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            # Kiểm tra xem mã đã tồn tại chưa
            if not self.search([('product_id', '=', new_id)]):
                return new_id