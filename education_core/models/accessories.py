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


class StudentAccessories(models.Model):
	_name = 'student.accessories'
	_description = 'Student Accessories'
	_order = 'id asc'
	_rec_name = 'name'

	name  = fields.Char(string='Name')
	studentClass = fields.Many2one('education.class',string='Class')
	accessoryLine_ids = fields.One2many('student.accessories.line', 'accessory_id' ,string='Accessory Type')
	
	_sql_constraints = [('studentClass_unique', 'unique(studentClass)',
						 'The class must be unique !')]
	totalPrice = fields.Float(compute="count_total",string="Total",store=True)
	
	@api.depends('accessoryLine_ids.accessoryPrice')
	def count_total(self):
		for rec in self:
			totalPrice = 0.0
			for line in rec.accessoryLine_ids:
				totalPrice+=line.accessoryPrice
			rec.totalPrice=totalPrice


class StudentAccessory(models.Model):
	_name = 'student.accessories.line'
	_description = 'Accessories Lines'
	_order = 'id asc'
	_rec_name = 'accessoryType'

	name = fields.Char(string='Name',readonly=True)
	quantity = fields.Float(string='Quantity',default=1.0)
	accessory_id = fields.Many2one('student.accessories',string='Accessory')
	accessoryType = fields.Many2one('student.accessories.type',string="Accessories Type",tracking=True,)
	accessoryPrice = fields.Float(related="accessoryType.totalPrice", string="price")
	gender_selector = fields.Selection([('shared', 'Shared'), ('male', 'Male'), ('female', 'Female')],
							  string='Gender selector', default='shared', required=True, track_visibility='onchange')

class StudentAccessoriesTypes(models.Model):
	_name = 'student.accessories.type'
	_description = 'Student Accessories Types'
	_order = 'id asc'
	_rec_name = 'name'

	name  = fields.Char(string='Name')
	studentClass = fields.Many2one('education.class',string='Class')
	accessorytype_ids = fields.One2many('student.accessories.type.line', 'accessory_type_id' ,string='Accessory Type')
	totalPrice = fields.Float(compute="count_total",string="Total",store=True)
	
	@api.depends('accessorytype_ids.totalPrice')
	def count_total(self):
		for rec in self:
			totalPrice = 0.0
			for line in rec.accessorytype_ids:
				totalPrice+=line.totalPrice
			rec.totalPrice=totalPrice

class StudentAccessoryTypeLines(models.Model):
	_name = 'student.accessories.type.line'
	_description = 'Accessories Types Lines'
	_order = 'id asc'
	_rec_name = 'accessoryType'

	name = fields.Char(string='Name',readonly=True)
	accessory_type_id = fields.Many2one('student.accessories.type',string='Accessory')
	accessoryType = fields.Many2one('product.product',string="Accessories Type")
	accessoryPrice = fields.Float(related="accessoryType.lst_price" ,string="Cost")
	quantity = fields.Float(string='Quantity',default=1.0)
	totalPrice = fields.Float(compute="count_total",string="Total")

	@api.depends('accessoryType','quantity')
	def count_total(self):
		for rec in self:
			totalPrice = 0.0
			if rec.accessoryType:
				totalPrice = rec.quantity*rec.accessoryPrice
			rec.totalPrice = totalPrice

