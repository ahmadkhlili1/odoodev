from odoo import fields, models, api
# from datetime import datetime
from datetime import date
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class offer(models.Model):
    _name = "estate_property_offer"
    _description = "This is a desc from kh "
    _order = "id desc"

    price = fields.Float()
    status = fields.Selection(string='Status', selection=[('Accepted', "Accepted"), ('Refused', "Refused")])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id =  fields.Many2one('estate_property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

    _sql_constraints = [
            ('check_selling_price', 'CHECK(price >= 0)', 'the price should be positive')
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        print(__name__)
        for record in self:
            try:
                record.date_deadline = timedelta(days=record.validity) + record.create_date
            except Exception:
                record.date_deadline = timedelta(days=record.validity) +  date.today()

    @api.depends('validity', 'create_date')
    def _inverse_deadline(self):
        print(__name__)
        for record in self:
            try:
                record.validity = (record.date_deadline -  record.create_date).days
            except Exception:
                # record.validity = (record.date_deadline - datetime.now()).days
                record.validity = (record.date_deadline - date.today()).days


    def accept_fun(self):
        for record in self:
                record.status = "Accepted"
                record.property_id.state = 'Offer Accepted'
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
                
        return True


    def decline_fun(self):
        for record in self:
                record.status = "Refused"
        return True
    
    @api.model
    def create(self, vals):
        # Do some business logic, modify vals...
        # Then call super to execute the parent method
        for record in self:
            if record.price < record.property_id.best_price:
                raise ValidationError(("You cannot add"))
        record.property_id.state = 'Offer Received'
        return super().create(vals)


