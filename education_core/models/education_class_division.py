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

from odoo.exceptions import ValidationError
from odoo import fields, models, api, _


class EducationClass(models.Model):
	_name = 'education.class'
	_description = "Standard"

	name = fields.Char(string='Name', required=True, help="Enter the Name of the Class")
	syllabus_ids = fields.One2many('education.syllabus', 'class_id')
	division_ids = fields.One2many('education.division', 'class_id')
	school_id = fields.Many2one('school.school', string='School')


class EducationDivision(models.Model):
	_name = 'education.division'
	_description = "Standard Division"

	name = fields.Char(string='Name', required=True, help="Enter the Name of the Division")
	strength = fields.Integer(string='Class Strength', help="Total strength of the class")
	faculty_id = fields.Many2one('education.faculty', string='Class Faculty', help="Class teacher/Faculty")
	class_id = fields.Many2one('education.class', string='Class')


class EducationClassDivision(models.Model):
	_name = 'education.class.division'
	_description = "Class room"

	# @api.model_create_multi
	# @api.model
	def create(self, vals):
		"""Return the name as a str of class + division"""
		# res = super(EducationClassDivision, self).create(vals)
		
		# class_id = self.env['education.class'].browse(vals['name'])
		class_id = self.env['education.class'].browse(vals['class_id'])
		# division_id = self.env['education.division'].browse(vals['name'])
		division_id = self.env['education.division'].browse(vals['division_id'])
		name = str(class_id.name + '-' + division_id.name)
		vals['name'] = name
		return super(EducationClassDivision, self).create(vals)

	@api.onchange('class_id','division_id')
	def _update_name(self):
		"""Return the name as a str of class + division"""
		if self.class_id and self.division_id:
			self.name = str(str(self.class_id.name) + '-' + str(self.division_id.name))		

	#@api.multi
	def view_students(self):
		"""Return the list of current students in this class"""
		self.ensure_one()
		students = self.env['education.student'].search([('class_id', '=', self.id)])
		students_list = students.mapped('id')
		self = self.with_context(class_id=self.id)
		return {
			'domain': [('id', 'in', students_list)],
			'name': _('Students'),
			# 'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'education.student',
			'view_id': False,
			'context': {'default_class_id': self.id},
			'type': 'ir.actions.act_window'
		}

	def _get_student_count(self):
		"""Return the number of students in the class"""
		for rec in self:
			students = self.env['education.student'].search([('class_id', '=', rec.id),('state','=','registered')])
			student_count = len(students) if students else 0
			rec.update({
				'student_count': student_count
			})
	gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
							  string='Gender', track_visibility='onchange')
	name = fields.Char(string='Name', readonly=True,compute='_update_name' ,store=True)
	actual_strength = fields.Integer(string='Class Strength', help="Total strength of the class")
	faculty_id = fields.Many2one('education.faculty', string='Class Faculty', help="Class teacher/Faculty")
	manager_id=fields.Many2one('education.faculty', string='Class Manager', help="Class teacher/Faculty")
	academic_year_id = fields.Many2one('education.academic.year', string='Academic Year',
									   help="Select the Academic Year", default=lambda self:self.env['education.academic.year'].search([('current_year','=',True)]), required=True)
	class_id = fields.Many2one('education.class', string='Class', required=True,
							   help="Select the Class")
	division_id = fields.Many2one('education.division', string='Division', required=True,
								  help="Select the Division")
	student_ids = fields.One2many('education.student', 'class_id', string='Students',domain=[('state','=','registered')])
	amenities_ids = fields.One2many('education.class.amenities', 'class_id', string='Amenities')
	student_count = fields.Integer(string='Students Count', compute='_get_student_count')
	school_id = fields.Many2one('school.school', string='School')
	active = fields.Boolean('Active', default=True,
							help="If unchecked, it will allow you to hide the class room without removing it.")
	next_school_id = fields.Many2one('school.school', string='Next School')

	@api.constrains('actual_strength')
	def validate_strength(self):
		"""Return Validation error if the students strength is not a non-zero number"""
		for rec in self:
			if rec.actual_strength <= 0:
				raise ValidationError(_('Strength must be a Non-Zero value'))

class EducationClassDivisionHistory(models.Model):
	_name = 'education.class.history'
	_description = "Class room history"
	_rec_name = 'class_id'

	academic_year_id = fields.Many2one('education.academic.year', string='Academic Year',
									   help="Select the Academic Year")
	class_id = fields.Many2one('education.class.division', string='Class Room',
							   help="Select the class")
	student_id = fields.Many2one('education.student', string='Students')


class EducationClassAmenities(models.Model):
	_name = 'education.class.amenities'
	_description = "Amenities in Class"

	name = fields.Many2one('education.amenities', string="Amenities",
						   help="Select the amenities in class room")
	qty = fields.Float(string='Quantity', help="The quantity of the amenities", default=1.0)
	class_id = fields.Many2one('education.class.division', string="Class Room")

	@api.constrains('qty')
	def check_qty(self):
		"""returns validation error if the qty is 0 or negative"""
		for rec in self:
			if rec.qty <= 0:
				raise ValidationError(_('Quantity must be Positive'))



# class CustomizedReport(models.TransientModel):
# 	_name = 'customized.report'

    
# 	model_id = fields.Many2one('ir.model', string='Model')
# 	field_ids = fields.Many2many('ir.model.fields', string='Fields' ,domain=[('model_id.model','=','education.student')])


# 	# def _active_id(self):
# 	# 	fields = ['']
# 	# 	domain=[('proposal_id', '=', active_id),('order_id','=',False)]
# 	# 	return domain

		


# class IrModelFields(models.Model):
# 	_inherit = 'ir.model.fields'
# 	_rec_name='field_description'
