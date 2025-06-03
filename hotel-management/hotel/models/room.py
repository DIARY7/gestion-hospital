# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Room(models.Model):
    _name = 'hotel.room'
    _description = 'Room generality'

    name = fields.Char(string='Number',required=True)
    room_category_id = fields.Many2one('hotel.room.category', string='Category',required=True)
    max_capacity = fields.Integer(string='Max capacity',required=True)
    equipment_ids = fields.Many2many('hotel.equipment', string='Equipments')  # Equipment default
    base_price = fields.Float(string='Price',required=True)
    total_price = fields.Float(string='Total Price',compute='_total_price')

    @api.depends('equipment_ids','room_category_id' )
    def _compute_total_price(self):
        for room in self:
            price_equipments = sum(room.equipment_ids.mapped('price'))
            room.total_price = (room.base_price * room.room_category_id.quality_level) + price_equipments

