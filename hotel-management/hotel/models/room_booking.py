# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class RoomBooking(models.Model):
    _name = 'hotel.room.booking'
    _description = "Room hotel's occupation"

    client_id = fields.Many2one('res.partner', string='Client',index=True,required=True)
    room_id = fields.Many2one('hotel.room', string='Room',index=True,required=True)
    nb_person = fields.Integer(string='Number of person',required=True)
    start_date = fields.Datetime(string='Start Date',required=True)
    end_date = fields.Datetime(string='End Date',required=True)
    equipment_add_ids = fields.Many2many('hotel.equipment', string='Equipments additional') # Equipment add plus add
    nights = fields.Integer(string='Number of night',required=True,readonly=True)
    state = fields.Selection([
        ('confirm'),
        ('cancel')
    ],)
    total_price = fields.Float(string='Total Price',readonly=True,compute='_compute_total_price',store = True) # Total night


    @api.depends('room_id','equipment_add_ids','start_date','end_date')
    def _compute_total_price(self):
        for booking in self:
            booking.total_price = (booking.room_id.total_price + sum(booking.equipment_add_ids.mapped('price')))*booking.nights

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for booking in self:
            if booking.start_date and booking.end_date:
                if booking.end_date <= booking.start_date:
                    raise UserError("La date de fin doit être postérieure à la date de début")

    @api.constrains('nb_person','room_id')
    def _check_room_capacity(self):
        for booking in self:
            if booking.nb_person <= 0:
                raise UserError("Le nombre de personne doit être correcté")

            if booking.room_id.max_capacity < booking.nb_person:
                raise UserError("Le nombre de personne dépasse la capacite maximale de la chambre")

    @api.constrains('room_id', 'start_date', 'end_date')
    def _check_room_availability(self):
        for booking in self:
            if booking.room_id and booking.start_date and booking.end_date:

                overlapping_bookings = self.search([
                    ('room_id', '=', booking.room_id.id),
                    ('id', '!=', booking.id),  # Exclure la réservation actuelle
                    ('start_date', '<', booking.end_date),
                    ('end_date', '>', booking.start_date),
                ])

                if overlapping_bookings:
                    raise UserError(
                        "La chambre est déjà réservée du %s au %s" % (
                            overlapping_bookings[0].start_date,
                            overlapping_bookings[0].end_date
                        )
                    )

    @api.depends('start_date','end_date')
    def _compute_nb_night(self):
        for booking in self:
            if booking.start_date and booking.end_date:
                start_date = booking.start_date.date()
                end_date = booking.end_date.date()

                delta = end_date - start_date
                booking.nights = delta.days
            else:
                booking.nights = 0

    def apply_all_compute(self):
        self._compute_nb_night()
        self._compute_total_price()

    def apply_all_constraints(self):
        self._check_dates()
        self._check_room_capacity()
        self._check_room_availability()