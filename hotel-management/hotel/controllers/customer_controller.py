# -*- coding: utf-8 -*-
from datetime import datetime
from pickle import FALSE

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
        categories = request.env['hotel.room.category'].search([])
        return request.render('hotel.landing_page',{
            'categories': categories
        })

    @http.route(['/book/form'], type='http', auth='user', website=True)
    def hotel_reserve(self, **kwargs):
        rooms = request.env['hotel.room'].search([])
        return request.render('hotel.form_booking',{
            'rooms': rooms,
            'values':{}
        })

    @http.route(['/my/book'], type='http', auth='user', website=True)
    def hotel_list_booking(self, **kwargs):
        room_bookings = request.env['hotel.room.booking'].search([
            ('client_id', '=' ,request.env.user.id)
        ])
        return request.render('hotel.list_booking_equipment', {
            'bookings': room_bookings,

        })

    @http.route(['/book/form/equipments'], type='http', auth='user', website=True ,  methods=['POST'], csrf=False)
    def hotel_reserve_equipment(self, **post):
        user = request.env.user
        Booking = request.env['hotel.room.booking']
        temp_booking = Booking.new({
            'client_id': user.id,
            'room_id': int(post.get('room_id')),
            'nb_person': int(post.get('nb_person')),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            # 'equipment_add_ids': [(6, 0, list(map(int, post.get('equipment_ids', []))))],
        })

        temp_booking.apply_all_compute()
        try:
            temp_booking.apply_all_constraints()

        except Exception as e:
            rooms = request.env['hotel.room'].search([])
            error = str(e)

            if 'start_date' in post:
                post['start_date'] = post['start_date'].split(' ')[0]

            if 'end_date' in post:
                post['end_date'] = post['end_date'].split(' ')[0]

            return request.render('hotel.form_booking', {
                'rooms': rooms,
                'values': post,
                'error': error
            },post)

        room = request.env['hotel.room'].browse(int(post.get('room_id')))
        all_equipments = request.env['hotel.equipment'].search([])
        room_equipments = room.equipment_ids  # Les équipements déjà dans la chambre
        available_equipments = all_equipments - room_equipments

        request.session['temp_booking'] = {
            'client_id': temp_booking.client_id.id,
            'room_id': temp_booking.room_id.id,
            'nb_person': temp_booking.nb_person,
            'start_date': temp_booking.start_date.isoformat(),
            'end_date': temp_booking.end_date.isoformat(),
            'equipment_add_ids': temp_booking.equipment_add_ids.ids,
            'nights': temp_booking.nights,
            'total_price': temp_booking.total_price,
        }

        return request.render('hotel.form_booking_equipment',{
            'nights':temp_booking.nights,
            'roomTotal':temp_booking.total_price,
            'room_equipments': room_equipments,
            'available_equipments': available_equipments,
        })

    @http.route(['/booking'], type='http', auth='user', website=True,csrf=False)
    def apply_reserve(self, **post):
        temp_booking = request.session.get('temp_booking')

        equipment_ids = post.get('equipment', '').split(',') if post.get('equipment') else []
        equipment_ids = [int(id) for id in equipment_ids if id.isdigit()]  # Filtrage et conversion

        if not temp_booking:
            return request.redirect('/book/form')

        # Convertit les données pour utilisation
        booking_data = {
            'client_id': int(temp_booking['client_id']),
            'room_id': int(temp_booking['room_id']),
            'nb_person': int(temp_booking['nb_person']),
            'start_date': datetime.fromisoformat(temp_booking['start_date']),
            'end_date': datetime.fromisoformat(temp_booking['end_date']),
            'equipment_add_ids': [(6, 0, equipment_ids)],
            'nights': int(temp_booking['nights']),
            'total_price': float(temp_booking['total_price']),
        }
        # Création réelle de la réservation
        booking = request.env['hotel.room.booking'].create(booking_data)
        request.session.pop('temp_booking', None)
        return request.render('hotel.form_booking_final')

    @http.route(['/my/book/cancel'], type='http', auth='user', website=True,csrf=False)
    def cancel_booking(self,**args):
        id_reservation = args.get('id_reservation')
        booking = request.env['hotel.room.booking'].browse(int(id_reservation))
        booking.write({
            'state': 'cancelled'  # Utilisez la valeur exacte définie dans votre Selection
        })
        return request.redirect('/my/book')





