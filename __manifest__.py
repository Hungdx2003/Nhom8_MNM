{
    'name': 'Quản lý kho hàng', 
    'version': '1.0',            
    'summary': 'Ứng dụng quản lý kho hàng',
    'description': '', 
    'author': 'nhom8',       
    'website': '',  
    'category': '',
    'depends': ['base'],
    'data': [
        'views/menu_views.xml', 
        'views/dashboard.xml',
        'views/product_view.xml',
        'views/inventory_views.xml',   
        'views/stock_in_views.xml', 
        'views/stock_in_line_views.xml',
        'views/stock_out_views.xml',
        'views/stock_out_line_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/web/static/lib/Chart/Chart.js',
            'static/src/js/dashboard_chart.js',
        ],
    },
    'installable': True,
    'application': True,    
}
