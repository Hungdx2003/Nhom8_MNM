odoo.define('nhom8.dashboard_chart', function(require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.ChartWidget = publicWidget.Widget.extend({
        selector: '.o_dashboard_chart',
        start: function() {
            this._renderChart();
        },
        _renderChart: function() {
            var stockInData = JSON.parse($('#stock_in_chart').data('stock_in_data'));  // Lấy dữ liệu từ view
            var stockOutData = JSON.parse($('#stock_out_chart').data('stock_out_data'));

            // Biểu đồ nhập kho
            var ctxStockIn = document.getElementById('stock_in_chart').getContext('2d');
            new Chart(ctxStockIn, {
                type: 'bar',
                data: {
                    labels: stockInData.map(function(item) { return item.label; }),
                    datasets: [{
                        label: 'Nhập kho',
                        data: stockInData.map(function(item) { return item.value; }),
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Biểu đồ xuất kho
            var ctxStockOut = document.getElementById('stock_out_chart').getContext('2d');
            new Chart(ctxStockOut, {
                type: 'bar',
                data: {
                    labels: stockOutData.map(function(item) { return item.label; }),
                    datasets: [{
                        label: 'Xuất kho',
                        data: stockOutData.map(function(item) { return item.value; }),
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    });
});
