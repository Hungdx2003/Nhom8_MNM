import json
from odoo import models, fields, api
from datetime import datetime, timedelta

class Dashboard(models.Model):
    _name = 'nhom8.dashboard'
    _description = 'Dashboard'

    total_product_quantity = fields.Integer(string="Tổng số lượng sản phẩm trong kho", compute="_compute_dashboard_data")
    total_inventory_value = fields.Float(string="Tổng giá trị tồn kho", compute="_compute_dashboard_data")
    monthly_stock_in_count = fields.Integer(string="Số lượng phiếu nhập trong tháng", compute="_compute_dashboard_data")
    monthly_stock_out_count = fields.Integer(string="Số lượng phiếu xuất trong tháng", compute="_compute_dashboard_data")
    top_stock_product = fields.Char(string="Sản phẩm tồn kho cao nhất", compute="_compute_dashboard_data")
    top_stock_quantity = fields.Integer(string="Số lượng tồn kho cao nhất", compute="_compute_dashboard_data")
    stock_in_chart_data = fields.Text(string="Dữ liệu biểu đồ nhập kho", compute="_compute_dashboard_data")
    stock_out_chart_data = fields.Text(string="Dữ liệu biểu đồ xuất kho", compute="_compute_dashboard_data")

    @api.depends()
    def _compute_dashboard_data(self):
        for record in self:
            # Tổng số lượng sản phẩm trong kho
            inventories = self.env['nhom8.inventory'].search([])
            record.total_product_quantity = sum(inventories.mapped('quantity'))

            # Tổng giá trị tồn kho
            record.total_inventory_value = sum(
                inventory.quantity * inventory.product_id.purchase_price
                for inventory in inventories
            )

            # Số lượng phiếu nhập và xuất trong tháng
            today = datetime.today().date()
            first_day_of_month = today.replace(day=1)
            last_day_of_month = (first_day_of_month.replace(month=today.month + 1, day=1) - timedelta(days=1))
            stock_in_records = self.env['nhom8.stock.in'].search([
                ('date_in', '>=', first_day_of_month),
                ('date_in', '<=', last_day_of_month)
            ])
            stock_out_records = self.env['nhom8.stock.out'].search([
                ('date_out', '>=', first_day_of_month),
                ('date_out', '<=', last_day_of_month)
            ])

            record.monthly_stock_in_count = len(stock_in_records)
            record.monthly_stock_out_count = len(stock_out_records)

            # Sản phẩm tồn kho cao nhất
            if inventories:
                top_product = max(inventories, key=lambda inv: inv.quantity)
                record.top_stock_product = top_product.product_id.name
                record.top_stock_quantity = top_product.quantity
            else:
                record.top_stock_product = "Không có sản phẩm"
                record.top_stock_quantity = 0

            # Lấy dữ liệu nhập kho trong tháng
            stock_in_lines = self.env['nhom8.stock.in.line'].search([
                ('stock_in_id.date_in', '>=', first_day_of_month),
                ('stock_in_id.date_in', '<=', last_day_of_month)
            ])
            stock_in_data = {}
            for line in stock_in_lines:
                date = line.stock_in_id.date_in.strftime('%Y-%m-%d')
                stock_in_data[date] = stock_in_data.get(date, 0) + line.quantity

            # Cập nhật dữ liệu cho biểu đồ nhập kho
            record.stock_in_chart_data = json.dumps([
                {'label': date, 'value': quantity} 
                for date, quantity in sorted(stock_in_data.items())
            ])

            # Tính dữ liệu xuất kho
            stock_out_lines = self.env['nhom8.stock.out.line'].search([
                ('stock_out_id.date_out', '>=', first_day_of_month),
                ('stock_out_id.date_out', '<=', last_day_of_month)
            ])
            stock_out_data = {}
            for line in stock_out_lines:
                date = line.stock_out_id.date_out.strftime('%Y-%m-%d')
                stock_out_data[date] = stock_out_data.get(date, 0) + line.quantity

            # Cập nhật dữ liệu cho biểu đồ xuất kho
            record.stock_out_chart_data = json.dumps([
                {'label': date, 'value': quantity} 
                for date, quantity in sorted(stock_out_data.items())
            ])
            
    def update_data(self):
        self._compute_dashboard_data()
