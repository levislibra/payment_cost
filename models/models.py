# -*- coding: utf-8 -*-

from openerp import models, fields, api

class payment_cost(models.Model):
	_inherit = 'account.payment'
	_name = 'account.payment'

	payment_cost = fields.Boolean('¿Tiene costo?')
	cost_communication = fields.Char('Motivo')
	cost_journal_id = fields.Many2one('account.journal', 'Diario')
	cost_percentage = fields.Float('Porcentaje del monto')
	cost_amount = fields.Float('Monto del costo', compute="_value_cost_amount")

	@api.depends('cost_percentage')
	def _value_cost_amount(self):
		if self.amount > 0 and self.cost_percentage > 0:
			self.cost_amount = self.amount * (self.cost_percentage / 100)