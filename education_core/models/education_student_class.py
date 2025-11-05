# -*- coding: utf-8 -*-
###################################################################################
#    A part of Educational ERP Project <https://www.educationalerp.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Nikhil krishnan (nikhil@cybrosys.in)
#            Niyas Raphy (niyas@cybrosys.in)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EducationStudentClass(models.Model):
	_name = 'education.student.class'
	_description = 'Assign the Students to Class'
	_inherit = ['mail.thread']
	_rec_name = 'class_id'

	class_id = fields.Many2one('education.class', string='Class')
	student_list = fields.One2many('education.student.list', 'connect_id', string="Students")
	admitted_class = fields.Many2one('education.class.division', string="Class Room")
	assigned_by = fields.Many2one('res.users', string='Assigned By', default=lambda self: self.env.uid)
	state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
							 string='Status', required=True, default='draft', track_visibility='onchange')
	school_id = fields.Many2one('school.school', string='School',default=lambda self: self.env['school.school'].search([('company_id','=',self.env.user.company_id.id)]))
	checkAll = fields.Boolean()
	class_strength = fields.Integer(related='admitted_class.actual_strength' ,readonly=True)
	free_seats = fields.Integer(readonly=True,compute='count_free_seats')
	counter = fields.Integer()

	@api.onchange('admitted_class')
	@api.depends('class_strength','admitted_class')
	def count_free_seats(self):
		for rec in self:
			if rec.admitted_class:
				rec.free_seats = rec.class_strength-rec.admitted_class.student_count
	
	#@api.multi
	@api.onchange('checkAll')
	def check_student(self):
		for rec in self:
			for student in rec.student_list:
				if self.checkAll==True:
					student.check_student=True
				if self.checkAll==False:
					student.check_student=False

	#@api.multi
	def unlink(self):
		"""Return warning if the Record is in done state"""
		for rec in self:
			if rec.state == 'done':
				raise ValidationError(_("Cannot delete Record in Done state"))

	#@api.multi
	def get_student_list(self):
		"""returns the list of students applied to join the selected class"""
		for rec in self:
			for line in rec.student_list:
				line.unlink()
			students = self.env['education.student'].search([
				('admission_class', '=', rec.class_id.id),
				('state', '=', 'registered'),('school_id','=',self.school_id.id)])
			if not students:
				raise ValidationError(_('No Students Available.. !'))
			values = []
			for stud in students:
				stud_line = {
					'class_id': rec.class_id.id,
					'student_id': stud.id,
					'connect_id': rec.id
				}
				values.append(stud_line)
			for line in values:
				student_line = self.env['education.student.list'].create(line)
				# rec.student_line = self.env['education.student.list'].create(line)

class EducationStudentList(models.Model):
	_name = 'education.student.list'
	_inherit = ['mail.thread']

	connect_id = fields.Many2one('education.student.class', string='Class Room')
	student_id = fields.Many2one('education.student', string='Student')
	class_id = fields.Many2one('education.class', string='Class')
	class_room = fields.Many2one('education.class.division',related='student_id.class_id', string='Class Room')
	previous_mark = fields.Float(string = 'Previous Mark',related='student_id.previous_mark')

	check_student = fields.Boolean()
	status = fields.Selection([('done','Done')],string='Done')
	prev_school = fields.Many2one('education.institute', string='Previous Institution',related="student_id.application_id.prev_school")

	#@api.multi
	def bulk_verify(self):
		lists=[]
		for record in self:
			record.check_student=True
		# 	lists.append(record.id)
		# raise ValidationError(_(lists))
