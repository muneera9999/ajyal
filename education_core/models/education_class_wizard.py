# -*- coding: utf-8 -*-
###################################################################################
#    A part of Educational ERP Project <https://www.educationalerp.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Niyas Raphy (niyas@cybrosys.in)
#            Nikhil krishnan (nikhil@cybrosys.in)
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


class ApplicationClassDetails(models.Model):
	_name = 'class.details'
	_description = "Student Allocation"

	student_class = fields.Many2one('education.class', string="Class", readonly=True,
									help="Select the Class to which the students applied")
	assigned_by = fields.Many2one('res.users', string='Assigned By', default=lambda self: self.env.uid,
								  help="Student Assigning is done by")
	class_id = fields.Many2one('education.class.division', string="Class Room", required=True,
							   help="Students are alloted to this Class", domain="[('class_id', '=', student_class)]")
	class_strength = fields.Integer(related='class_id.actual_strength',readonly=True)
	free_seats = fields.Integer(readonly=True,store=True,compute='count_free_seats')

	#@api.multi
	def action_assign_class(self):
		"""Assign the class for the selected students after admission by the faculties"""
		for rec in self:
			assign_request = self.env['education.student.class'].browse(self.env.context.get('active_ids'))
			student_list = assign_request.student_list.filtered(lambda rec: rec.check_student ==True)
			if len(student_list)>self.free_seats:
					raise ValidationError(_('Free seats in this class less than students in list'))
			else:
				# assign_request.get_student_list()
				if not assign_request.student_list:
					raise ValidationError(_('No Student Lines'))
				for line in assign_request.student_list:
					if line.check_student==True:
						line.student_id.class_id = rec.class_id.id
						line.status='done'
						assign_request.write({
							# 'state': 'done',
							'admitted_class': rec.class_id.id,
							'assigned_by': rec.assigned_by.id
						})
	@api.onchange('class_id')
	@api.depends('class_strength','class_id')
	def count_free_seats(self):
		for rec in self:
			if rec.class_id:
				rec.free_seats = rec.class_strength-rec.class_id.student_count
	