from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class TestModel(models.Model):
    _name = "estate_property"
    _description = "This is a desc from kh "
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Last Seen", default=lambda self: fields.Datetime.now())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, default=0)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean('Active', default=False)
    garden_orientation = fields.Selection(string='Garden orientation', selection=[('North', "North"), ('South', "South"), ('East', "East"), ('West', "West")])
    state = fields.Selection(string='State',required=True, copy=False,default="New", selection=[('New', "New"), ('Offer Received', "Offer Received"), ('Offer Accepted', "Offer Accepted"), ('Sold', "Sold"), ('Canceled',"Canceled")])
    property_type_id = fields.Many2one('estate_property_type', string='Property type')
    buyer = fields.Many2one('res.partner', copy=False, string='Buyer' )
    seller = fields.Many2one('res.users', string ='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate_property_tag')
    offer_ids = fields.One2many('estate_property_offer', 'property_id', string ='oFFer')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Integer(compute='_max_price', defualt=0)
    user_id = fields.Many2one('res.users')
    # status = fields.Char(readonly=True)




    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'the price should be positive')

    ]


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends('offer_ids.price')
    def _max_price(self):
        if len([i.price for i in self.offer_ids]) > 0:
            self.best_price = max([i.price for i in self.offer_ids])
        else:
             self.best_price = 0
        # for record in self.offer_ids:
            # record.best_price = max(record)

    def sold_fun(self):
        for record in self:
            if record.state == 0:
                record.state = "SOLD"
            else:
                raise UserError (('cancel cannot be sold.'))
        return True

    def cancel_fun(self):
        for record in self:
            if record.state == 0:
                record.state = "CANCEL"
            else:
               raise UserError (('Sold cannot be cancel.'))
                
        return True
    


    @api.constrains('selling_price', 'expected_price')
    def _check_percent(self):
        for term_line in self:
            if term_line.selling_price <= 0.90 * term_line.expected_price and  term_line.state == 'Sold':
                raise ValidationError(("Percentages on the selling price must be more than %90 from expected price."))
    
    @api.model
    def delete(self, vals):
        # Do some business logic, modify vals...
        # Then call super to execute the parent method
        for record in self:
            if record.state != 'New' or 'Canceled':
                return super().delete(vals)

