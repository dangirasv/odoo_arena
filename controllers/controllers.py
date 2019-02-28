# -*- coding: utf-8 -*-
from odoo import http

# class Odooarena(http.Controller):
#     @http.route('/odooarena/odooarena/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odooarena/odooarena/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odooarena.listing', {
#             'root': '/odooarena/odooarena',
#             'objects': http.request.env['odooarena.odooarena'].search([]),
#         })

#     @http.route('/odooarena/odooarena/objects/<model("odooarena.odooarena"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odooarena.object', {
#             'object': obj
#         })