# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Room(models.Model):
    _name = 'hotel.room'
    _description = 'Room generality'

    name = fields.Char(string='Number',required=True)
    room_category_id = fields.Many2one('hotel.room.category', string='Category',index=True,required=True)
    max_capacity = fields.Integer(string='Max capacity',required=True)
    equipment_ids = fields.Many2many('hotel.equipment', string='Equipments')  # Equipment default
    total_price = fields.Float(string='Total Price',compute='_compute_total_price') # one night

    @api.depends('equipment_ids','room_category_id','room_category_id.base_price' )
    def _compute_total_price(self):
        for room in self:
            price_equipments = sum(room.equipment_ids.mapped('price'))
            room.total_price =  room.room_category_id.base_price + price_equipments
