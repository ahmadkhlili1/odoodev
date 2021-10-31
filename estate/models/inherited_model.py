from odoo import fields, models

class InheritedModel(models.Model):
    # _inherit = "inherited.model"
    _inherit = "estate_property"
    property_ids = fields.One2many('estate_property', 'user_id', string ='Inherited')