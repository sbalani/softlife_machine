from odoo import fields, models


class SoftlifeMachineTransferWizard(models.TransientModel):
    _name = 'softlife.machine.transfer.wizard'
    _description = 'Assign / Transfer a Machine'

    machine_id = fields.Many2one('softlife.machine', required=True)
    from_partner_id = fields.Many2one('res.partner', string='From Customer', readonly=True)
    from_location_id = fields.Many2one('stock.location', string='From Location', readonly=True)
    to_partner_id = fields.Many2one('res.partner', string='To Customer', required=True)
    to_location_id = fields.Many2one('stock.location', string='To Location', required=True)
    to_warehouse_id = fields.Many2one('stock.warehouse', string='Serving Warehouse')
    note = fields.Text()

    def action_apply(self):
        """Create a numbered transfer/delivery document and update the machine."""
        self.ensure_one()
        machine = self.machine_id
        self.env['softlife.machine.transfer'].create({
            'machine_id': machine.id,
            'from_partner_id': self.from_partner_id.id,
            'from_location_id': self.from_location_id.id,
            'to_partner_id': self.to_partner_id.id,
            'to_location_id': self.to_location_id.id,
            'note': self.note,
        })
        machine.write({
            'partner_id': self.to_partner_id.id,
            'location_id': self.to_location_id.id,
            'warehouse_id': self.to_warehouse_id.id or machine.warehouse_id.id,
        })
        return {'type': 'ir.actions.act_window_close'}
