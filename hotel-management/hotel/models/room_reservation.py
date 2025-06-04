# -*- coding: utf-8 -*-
from odoo import models, fields, api

class RoomReservation(models.Model):
    _name = 'hotel.room.reservation'
    _description = "Room hotel's occupation"

    client_id = fields.Many2one('res.partner', string='Client',required=True)
    room_id = fields.Many2one('hotel.room', string='Room',required=True)
    nb_person = fields.Integer(string='Number of person',required=True)
    start_date = fields.Datetime(string='Start Date',required=True)
    end_date = fields.Datetime(string='End Date',required=True)
    equipment_add_ids = fields.Many2many('hotel.equipment', string='Equipments additional') # Equipment add plus add
    total_price = fields.Float(string='Total Price',readonly=True,compute='_compute_total_price')

    @api.depends('room_id','equipment_add_ids')
    def _compute_total_price(self):
        for reservation in self:
            reservation.total_price = reservation.room_id.total_price + sum(reservation.equipment_add_ids.mapped('total_price'))


    def is_reserved(self,room_id,start_date,end_date): # start_date and end_date of demand
        print('is_reserved')