from odoo import fields, models

class Type(models.Model):
        _name = "estate_property_type"
        _description = "This is a desc from kh "
        _order = "sequence, name"

        name = fields.Char(required=True)
        sequence =fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
        _sql_constraints = [
            ('check_name', 'UNIQUE(name)', 'the name must be unique')
    ]
        property_ids = fields.One2many('estate_property', 'property_type_id')