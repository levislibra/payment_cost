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
	cost_move_id = fields.Many2one('account.move', default=None)

	@api.depends('cost_percentage')
	def _value_cost_amount(self):
		if self.amount > 0 and self.cost_percentage > 0:
			self.cost_amount = self.amount * (self.cost_percentage / 100)

	@api.one
	def confirm_cost(self):
		if self.payment_cost == True and self.state != 'osted' and len(self.cost_move_id) == 0:
			line_ids = []
			if self.payment_type == "outbound" or self.payment_type == "transfer":
				# Cuando realizamos el pago a un proveedor o una transferencia interna
				# el costo del pago nos genera un egreso.
				account_id = None
				if self.payment_type == "outbound":
					account_id = self.partner_id.property_account_payable_id.id
				elif self.payment_type == "transfer":
					account_id = self.destination_journal_id.default_debit_account_id.id
				# Registramos el costo a favor del proveedor o decrementamos la cuenta destino
				aml = {
				    'date': self.payment_date,
				    'account_id': account_id,
				    'name': self.cost_communication,
				    'partner_id': self.partner_id.id,
				    'credit': self.cost_amount,
				    #'journal_id': self.
				}
				line_ids.append((0,0,aml))

				# Registramos el costo como gasto en el diario seleccionado
				aml2 = {
				    'date': self.payment_date,
				    'account_id': self.cost_journal_id.default_debit_account_id.id,
				    'name': self.cost_communication,
				    'partner_id': self.partner_id.id,
				    'debit': self.cost_amount,
				    #'journal_id': self.
				}
				line_ids.append((0,0,aml2))
			elif self.payment_type == "inbound":
				# Cuando registramos el pago de un cliente
				# el costo del pago nos genera un ingreso.

				# Registramos el costo como un ingreso en el diario seleccionado
				aml = {
				    'date': self.payment_date,
				    'account_id': self.cost_journal_id.default_debit_account_id.id,
				    'name': self.cost_communication,
				    'partner_id': self.partner_id.id,
				    'credit': self.cost_amount,
				    #'journal_id': self.
				}
				line_ids.append((0,0,aml))

				# Registramos el costo disminuyendo la cuenta del cliente
				aml2 = {
				    'date': self.payment_date,
				    'account_id': self.partner_id.property_account_receivable_id.id,
				    'name': self.cost_communication,
				    'partner_id': self.partner_id.id,
				    'debit': self.cost_amount,
				    #'journal_id': self.
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
			self.cost_move_id = move
