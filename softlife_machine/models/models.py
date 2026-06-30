from odoo import api, fields, models


class SoftlifeMachine(models.Model):
    _name = 'softlife.machine'
    _description = 'Soft-serve Machine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(required=True, tracking=True)
    ref = fields.Char(string='Internal Reference')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company, required=True,
    )
    state = fields.Selection(
        [('active', 'Active'), ('in_transit', 'In Transit'),
         ('stored', 'In Storage'), ('retired', 'Retired')],
        default='active', tracking=True,
    )

    # --- Huaxin link (populated by softlife_huaxin) ---
    device_imei = fields.Char(string='Huaxin IMEI', index=True, tracking=True)
    device_id_huaxin = fields.Char(string='Huaxin Device ID')

    # --- Assignment (one customer may host several machines) ---
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    location_id = fields.Many2one('stock.location', string='Current Location', tracking=True)
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Serving Warehouse', tracking=True,
        help='Warehouse that refills this machine. One warehouse may serve many machines.',
    )

    # --- Product / hopper configuration ---
    base_product_id = fields.Many2one(
        'product.product', string='Base Product', tracking=True,
        help='Ice-cream base vs yoghurt base, etc.',
    )
    ingredient_line_ids = fields.One2many(
        'softlife.machine.ingredient', 'machine_id', string='Hoppers / Ingredients',
    )
    ingredient_count = fields.Integer(compute='_compute_ingredient_count')

    # --- HACCP-relevant maintenance facts (written by softlife_haccp) ---
    last_full_clean_date = fields.Datetime(string='Last Full Clean', tracking=True)

    # --- Transfer / delivery history ---
    transfer_ids = fields.One2many('softlife.machine.transfer', 'machine_id', string='Transfers')
    transfer_count = fields.Integer(compute='_compute_transfer_count')

    @api.depends('ingredient_line_ids')
    def _compute_ingredient_count(self):
        for rec in self:
            rec.ingredient_count = len(rec.ingredient_line_ids)

    @api.depends('transfer_ids')
    def _compute_transfer_count(self):
        for rec in self:
            rec.transfer_count = len(rec.transfer_ids)

    def action_open_transfers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfers',
            'res_model': 'softlife.machine.transfer',
            'view_mode': 'list,form',
            'domain': [('machine_id', '=', self.id)],
            'context': {'default_machine_id': self.id},
        }

    def action_transfer(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assign / Transfer Machine',
            'res_model': 'softlife.machine.transfer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_machine_id': self.id,
                'default_from_partner_id': self.partner_id.id,
                'default_from_location_id': self.location_id.id,
            },
        }


class SoftlifeMachineIngredient(models.Model):
    _name = 'softlife.machine.ingredient'
    _description = 'Machine Hopper / Ingredient Configuration'
    _order = 'position, id'

    machine_id = fields.Many2one('softlife.machine', required=True, ondelete='cascade')
    position = fields.Char(
        required=True,
        help='Hopper/lane position. Maps to the Huaxin product position (e.g. 1, 2, topping_1).',
    )
    product_id = fields.Many2one('product.product', required=True)
    product_type = fields.Selection(
        [('base', 'Base'), ('topping', 'Topping'), ('sauce', 'Sauce')],
        default='topping',
    )
    enabled = fields.Boolean(default=True)
    cycled = fields.Boolean(
        string='Cycles',
        help='True if this hopper rotates among different products over time.',
    )
    portion_size = fields.Float(
        string='Portion Size',
        help='Fixed dispense portion (Decision #5: portion sizes are per-machine).',
    )
    loaded_capacity = fields.Float(
        string='Loaded Capacity',
        help='Quantity loaded at a full refill; basis for the 30% refill alert.',
    )


class SoftlifeMachineTransfer(models.Model):
    _name = 'softlife.machine.transfer'
    _description = 'Machine Transfer / Delivery Document'
    _inherit = ['mail.thread']
    _order = 'date desc'

    name = fields.Char(string='Delivery Ref', required=True, copy=False, readonly=True, default=lambda self: 'New')
    machine_id = fields.Many2one('softlife.machine', required=True, ondelete='cascade', tracking=True)
    date = fields.Datetime(default=fields.Datetime.now, required=True)
    from_partner_id = fields.Many2one('res.partner', string='From Customer')
    to_partner_id = fields.Many2one('res.partner', string='To Customer', required=True)
    from_location_id = fields.Many2one('stock.location', string='From Location')
    to_location_id = fields.Many2one('stock.location', string='To Location', required=True)
    note = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('softlife.machine.transfer') or 'New'
        return super().create(vals_list)
