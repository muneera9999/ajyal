# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class StudentTransfer(models.TransientModel):
	_name = "student.transfer"
	_description = "Student Transfering"



	class_id = fields.Many2one('education.class', string='Class')
	division_id = fields.Many2one('education.class.division', 'Division')
	academic_year = fields.Many2one('education.academic.year',string='Academic Year',required=True,
											default=lambda self: self.env['education.academic.year'].search([('current_year','=',True)]))
	school_id = fields.Many2one('school.school', string='School')
	target_move = fields.Selection([('division', 'Division To Division'),
									 ('class', 'Class To Class'),('school','School To School')
									], string='Transfer type', required=True)


	def action_transfer(self):
		active_id = self._context.get('active_id')
		student_id  = self.env['education.student'].search([('id','=',active_id)])
		if student_id:
			if self.target_move=='class' and self.class_id:
				student_id.write({'admission_class':self.class_id.id})
				# student_id.write({'admission_class':self.class_id.id,'class_id':False})
			elif self.target_move=='division' and self.division_id:
				student_id.write({'class_id':self.division_id.id})
			elif self.target_move=='class' and self.division_id and self.class_id:
				student_id.write({'admission_class':self.class_id.id,'class_id':self.division_id.id})
			elif self.target_move=='school' and self.school_id:
				student_id.write({'school_id':self.school_id.id,'admission_class':False})
				# student_id.write({'school_id':self.school_id.id,'class_id':False,'admission_class':False})


	#@api.multi
	def _school_default_get(self):
		school_id = 0
		if self.class_id:
			
			for rec in self.class_id:
				school_id = rec.class_id

		return school_id