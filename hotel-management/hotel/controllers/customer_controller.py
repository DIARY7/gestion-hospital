# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class CustomerController(http.Controller):
    @http.route(['/my'], type='http', auth='user', website=True)
    def redirect_portal(self, **kwargs):
        user = request.env.user

        # Si l'utilisateur appartient au groupe 'portal'
        if user.has_group('base.group_portal'):
            return request.redirect('/my/hotel')

        # Sinon, garder le comportement par défaut
        return request.redirect('/')

    @http.route(['/my/hotel'], type='http', auth='user', website=True)
    def hotel_landing(self, **kwargs):

        return request.render('hotel.landing_page')


