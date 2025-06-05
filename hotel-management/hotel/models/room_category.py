# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RoomCategory(models.Model):
    _name = 'hotel.room.category'
    _description = "The hotel's room categories"

    name = fields.Char(string='Name',required=True)
    base_price = fields.Float(string="Base price",required=True)




