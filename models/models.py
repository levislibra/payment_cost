# -*- coding: utf-8 -*-

from openerp import models, fields, api

class payment_cost(models.Model):
	_inherit = 'account.payment'
	_name = 'account.payment'

	payment_cost = fields.Boolean('¿Tiene costo?', related='payment_desc')
	payment_desc = fields.Boolean('¿Tiene descuento?')
	cost_communication = fields.Char('Motivo')
	cost_journal_id = fields.Many2one('account.journal', 'Diario', domain="[('type', '=', 'purchase')]")
	cost_percentage = fields.Float('Porcentaje')
	cost_amount = fields.Float('Monto')
	cost_move_id = fields.Many2one('account.move', 'Asiento', default=None)
	cost_move_boolean = fields.Boolean(default=False)

	@api.depends('cost_percentage')
	@api.onchange('cost_percentage')
	def _change_cost_amount(self):
		if (self.amount > 0 or self.readonly_amount > 0) and self.cost_percentage > 0:
			self.cost_amount = self.amount * (self.cost_percentage / 100)

	@api.one
	def copy(self, default=None):
		default = dict(default or {})
		default.update({
			'cost_move_id': None,
			'cost_move_boolean': False,
		})
		return super(payment_cost, self).copy(default)

	@api.one
	def confirm_cost(self):
		if self.payment_cost == True and self.state == 'posted' and len(self.cost_move_id) == 0:
			line_ids = []
			if self.payment_type == "outbound":
				# Cuando realizamos el pago a un proveedor o un cliente
				
				if self.partner_type == "supplier":
					# Pago a un proveedor - genera un costo
					# Registramos el monto a favor del proveedor, lo cual nos generara un
					# costo
					aml = {
					    'date': self.payment_date,
					    'account_id': self.partner_id.property_account_payable_id.id,
					    'name': self.cost_communication,
					    'partner_id': self.partner_id.id,
					    'credit': self.cost_amount,
					    'journal_id': self.cost_journal_id.id,
					}
					line_ids.append((0,0,aml))

					# Registramos el costo como gasto en el diario seleccionado
					aml2 = {
					    'date': self.payment_date,
					    'account_id': self.cost_journal_id.default_debit_account_id.id,
					    'name': self.cost_communication,
					    'partner_id': self.partner_id.id,
					    'debit': self.cost_amount,
					    'journal_id': self.cost_journal_id.id,
					}
					line_ids.append((0,0,aml2))
				elif self.partner_type == "customer":
					# Pago a un cliente - genera un descuento

					# Registramos el monto a favor del cliente, lo cual genera un
					# descuento
					aml = {
					    'date': self.payment_date,
					    'account_id': self.partner_id.property_account_receivable_id.id,
					    'name': self.cost_communication,
					    'partner_id': self.partner_id.id,
					    'credit': self.cost_amount,
					    'journal_id': self.cost_journal_id.id,
					}
					line_ids.append((0,0,aml))

					# Registramos el costo disminuyendo la cuenta del cliente
					aml2 = {
					    'date': self.payment_date,
					    'account_id': self.cost_journal_id.default_debit_account_id.id,
					    'name': self.cost_communication,
					    'partner_id': self.partner_id.id,
					    'debit': self.cost_amount,
					    'journal_id': self.cost_journal_id.id,
					}
					line_ids.append((0,0,aml2))


			# create move
			company_id = self.env['res.users'].browse(self.env.uid).company_id.id
			move_name = "COST/"
			move = self.env['account.move'].create({
			'name': move_name,
			'date': self.payment_date,
			'journal_id': self.cost_journal_id.id,
			'state':'draft',
			'company_id': company_id,
			'partner_id': self.partner_id.id,
			'line_ids': line_ids,
			})
			move.name = move_name + str(move.id)
			move.state = 'posted'
			self.cost_move_id = move.id
			self.cost_move_boolean = True
