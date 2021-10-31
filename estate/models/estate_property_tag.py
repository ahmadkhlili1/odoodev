from odoo import fields, models

class Tag(models.Model):
    _name = "estate_property_tag"
    _description = "This is a desc from kh "
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
            ('check_name', 'UNIQUE(name)', 'the name must be unique')
    ]
