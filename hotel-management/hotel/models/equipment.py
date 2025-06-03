# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Equipment(models.Model):
    _name = 'hotel.equipment'
    _description = 'Hotel Equipment'

    name = fields.Char(string='Name',required=True)
    price = fields.Float(string='Price',required=True)



