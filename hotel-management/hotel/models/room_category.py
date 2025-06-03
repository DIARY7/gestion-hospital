# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RoomCategory(models.Model):
    _name = 'hotel.room.category'
    _description = "The hotel's room categories"

    name = fields.Char(string='Nom',required=True)
    quality_level = fields.Float(string="Quality level",required=True)




