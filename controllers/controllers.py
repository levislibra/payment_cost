# -*- coding: utf-8 -*-
from openerp import http

# class PaymentCost(http.Controller):
#     @http.route('/payment_cost/payment_cost/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_cost/payment_cost/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_cost.listing', {
#             'root': '/payment_cost/payment_cost',
#             'objects': http.request.env['payment_cost.payment_cost'].search([]),
#         })

#     @http.route('/payment_cost/payment_cost/objects/<model("payment_cost.payment_cost"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_cost.object', {
#             'object': obj
#         })