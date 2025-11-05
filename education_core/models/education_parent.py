# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api, _
# from odoo.exceptions import Warning
from odoo.exceptions import ValidationError

class OpParent(models.Model):
	_name = 'op.parent'
	_inherits = {'res.partner': 'parttner_id'}


	@api.model_create_multi
	# @api.model
	def create(self, vals):
		"""Over riding the create method to assign
		the sequence for newly creating records"""
		# vals['Driver_number'] = self.env['ir.sequence'].next_by_code('driver.driver')
		vals['is_parent'] = True

		res = super(OpParent, self).create(vals)
		return res

		

	parttner_id = fields.Many2one(
		'res.partner', string='Partner', required=True, ondelete="cascade")

	# name = fields.Char('Name', required=True)
	user_id = fields.Many2one('res.users', string='User', store=True)
	email = fields.Char(string='Email')
	phone = fields.Char(string='Phone')

	student_ids = fields.One2many('education.student','parent_ids', string='Student(s)',domain=[('state','!=','alumni'),('state','!=','transfer')])

	career = fields.Char(string='Parent career')
	mobile = fields.Char(string='Mobile')
	address = fields.Char(string='Address')
	# relationship = fields.Char(string='Relationship')
	childs_no = fields.Integer(string='Childs Counter', compute='compute_childs_number') 


	def action_is_parent(self):
		students = self.env['op.parent'].search([('id','>=',0)])
		for  rec in students:
			if rec.parttner_id.is_parent == False:
				rec.parttner_id.write({'is_parent':True})
			if rec.parttner_id.company_type == 'company':
				rec.parttner_id.write({'is_company':False,'company_type':'person'})
	# @api.onchange('name')
	# def set_company_onchange(self):
	# 	for rec in self:
	# 		rec.is_company = True
	# 		rec.company_type = 'company'

	@api.depends('student_ids')
	def compute_childs_number(self):
		for rec in self:
			rec.childs_no = len(rec.student_ids)
			


	# @api.model_create_multi
	# @api.model
	def create(self, vals):
		res = super(OpParent, self).create(vals)
		if vals.get('student_ids', False) and res.user_id:
			student_ids = self.student_ids.browse(res.student_ids.ids)
			user_ids = [student_id.user_id.id for student_id in student_ids
						if student_id.user_id]
			res.user_id.child_ids = [(6, 0, user_ids)]
			# vals['is_company'] = True
		return res

	#@api.multi
	def write(self, vals):
		for record in self:
			res = super(OpParent, self).write(vals)
			if vals.get('student_ids', False) and record.user_id:
				student_ids = record.student_ids.browse(record.student_ids.ids)
				user_ids = [student_id.user_id.id for student_id in student_ids
							if student_id.user_id]
				record.user_id.child_ids = [(6, 0, user_ids)]
			record.clear_caches()
			return res

	# def unlink(self):
	# 	for rec in self:
	# 		rec.parttner_id.unlink()
	# 	return super(OpParent, self).unlink()

	# #@api.multi
	# def unlink(self):
	# 	for record in self:
	# 		if record.user_id:
	# 			record.user_id.child_ids = [(6, 0, [])]
	# 		return super(OpParent, self).unlink()

	#@api.multi
	def create_parent_user(self):
		for record in self:
			if not record.email:
				raise ValidationError(_('Update parent email id first.'))
			if not record.user_id:
				groups_id = self.env.ref(
					'education_core.parent_template_user') and self.env.ref(
					'education_core.parent_template_user'
				).groups_id or False
				user_id = self.env['res.users'].create(
					{'name': record.name, 'partner_id': record.id,
					 'login': record.email, 'groups_id': groups_id})
				record.user_id = user_id
				user_ids = [
					x.user_id.id for x in record.student_ids if x.user_id]
				record.user_id.child_ids = [(6, 0, user_ids)]


class OpStudent(models.Model):

	_inherit = 'education.student'

	# parent_ids = fields.Many2one('op.parent', string='Parent')

	# @api.model_create_multi
	# @api.model
	def create(self, vals):
		res = super(OpStudent, self).create(vals)
		if vals.get('parent_ids', False):
			for parent_id in res.parent_ids:
				if parent_id.user_id:
					user_ids = [x.user_id.id for x in parent_id.student_ids
								if x.user_id]
					parent_id.user_id.child_ids = [(6, 0, user_ids)]
		return res

	# #@api.multi
	# def write(self, vals):
	# 	res = super(OpStudent, self).write(vals)
	# 	if vals.get('parent_ids', False):
	# 		user_ids = []
	# 		if self.parent_ids:
	# 			for parent_id in self.parent_ids:
	# 				if parent_id.user_id:
	# 					user_ids = [x.user_id.id for x in parent_id.student_ids
	# 								if x.user_id]
	# 					parent_id.user_id.child_ids = [(6, 0, user_ids)]
	# 		else:
	# 			user_ids = self.env['res.users'].search([
	# 				('child_ids', 'in', self.user_id.id)])
	# 			for user_id in user_ids:
	# 				child_ids = user_id.child_ids.ids
	# 				child_ids.remove(self.user_id.id)
	# 				user_id.child_ids = [(6, 0, child_ids)]
	# 	if vals.get('user_id', False):
	# 		for parent_id in self.parent_ids:
	# 			child_ids = parent_id.user_id.child_ids.ids
	# 			child_ids.append(vals['user_id'])
	# 			parent_id.user_id.child_ids = [(6, 0, child_ids)]
	# 	self.clear_caches()
	# 	return res

	# #@api.multi
	# def unlink(self):
	# 	for record in self:
	# 		if record.parent_ids:
	# 			for parent_id in record.parent_ids:
	# 				child_ids = parent_id.user_id.child_ids.ids
	# 				child_ids.remove(record.user_id.id)
	# 				parent_id.user_id.child_ids = [(6, 0, child_ids)]
	# 	return super(OpStudent, self).unlink()




