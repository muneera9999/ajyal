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
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
0.00

class EducationStudent(models.Model):
	_name = 'education.student'
	_inherit = ['mail.thread']
	_inherits = {'res.partner': 'partner_id'}
	_description = 'Student record'
	_rec_name = 'name'
	_order='name asc'


	#@api.multi
	def action_rigster(self):
		self.write({'state':'registered'})


	#@api.multi
	def action_alumni(self):
		self.write({'state':'alumni'})
		self.class_id==False;

	#@api.multi
	def action_pendent(self):
		self.write({'state':'pendent'})

	#@api.multi
	def action_leave(self):
		self.write({'state':'leave'})
		# self.write({'state':'leave','class_id':False})
	
	def action_is_student(self):
		students = self.env['education.student'].search([('id','>=',0)])
		for  rec in students:
			if rec.partner_id.is_student == False:
				rec.partner_id.write({'is_student':True})
			rec.parent_id=	False

		# partners = self.env['res.partner'].search([('is_student','=',True)])
		# for rec in partners:
		# 	student = self.env['res.partner'].search_count([('name','=',rec.name)])
		# 	if student == 0:
		# 		rec.unlink()

			# rec.parent_id = rec.parent_ids.parttner_id.id

	# def unlink(self):
	# 	for rec in self:
	# 		rec.partner_id.unlink()
	# 	return super(EducationStudent, self).unlink()


	#@api.multi
	def student_documents(self):
		"""Return the documents student submitted
		along with the admission application"""
		self.ensure_one()
		# if self.application_id.id:
		# documents = self.env['education.documents'].search([('application_ref', '=', self.application_id.id)])
		# documents_list = documents.mapped('id')
		return {
			'domain': [('student_id', '=', self.id)],
			'name': _('Documents'),
			# 'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'education.documents',
			'view_id': False,
			'context': {'create':True,'default_student_id': self.id},
			'type': 'ir.actions.act_window'
			}
	# def _compute_full_name(self):
	# 	for record in self:
	# 		record.full_name = f"{record.first_name or ''} {record.middle_name or ''} {record.last_name or ''}".strip() ##### muneera

	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		if name:
			recs = self.search([('name', operator, name)] + (args or []), limit=limit)
			if not recs:
				recs = self.search([('ad_no', operator, name)] + (args or []), limit=limit)
			return recs.name_get()
		return super(EducationStudent, self).name_search(name, args=args, operator=operator, limit=limit)

	# @api.model_create_multi
	# @api.model
	def create(self, vals):
		"""Over riding the create method to assign sequence for the newly creating the record"""
		vals['ad_no'] = self.env['ir.sequence'].next_by_code('education.student')
		vals['is_student'] = True

		res = super(EducationStudent, self).create(vals)
		return res

	# def class_id_domain(self):
	# 	self.class_id = False
	# 	domain = {'class_id': [('class_id', '=', self.admission_class.id),('gender', '=', self.gender),('school_id', '=', self.school_id)]}
	# 	return {'domain': domain}

	partner_id = fields.Many2one(
		'res.partner', string='Partner', required=True, ondelete="cascade")
	middle_name = fields.Char(string='Middle Name')
	second_name = fields.Char(string='Second Name')
	last_name = fields.Char(string='Last Name')
	# application_no = fields.Char(string="Application No")
	date_of_birth = fields.Date(string="Date Of birth", requird=False)
	parent_ids = fields.Many2one('op.parent', string="Guardian")
	father_name = fields.Char(string="Father")
	mother_name = fields.Char(string="Mother")
	# class_id = fields.Many2one('education.class.division', string="Class Room")	
	class_id = fields.Many2one('education.class.division', string="Class Room", required=True)	
#   domain="[('class_id', '=', admission_class),('school_id', '=',school_id)]"
	admission_class = fields.Many2one('education.class', string="Class")
	# ad_no = fields.Integer(string="Admission Number", readonly=True)
	ad_no = fields.Char(string="Admission Number", readonly=True)
	gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
							  string='Gender', required=True, track_visibility='onchange')
	blood_group = fields.Selection([('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'), ('o-', 'O-'),
									('ab-', 'AB-'), ('ab+', 'AB+')],
								   string='Blood Group', required=False, track_visibility='onchange')
	academic_year_id = fields.Many2one('education.academic.year', string='Academic Year',
									   help="Choose Academic year for which the admission is choosing",
									  default=lambda self:self.env['education.academic.year'].search([('current_year','=',True)]) ) ##### muneera
	school_id = fields.Many2one('school.school', string='School')
	per_street = fields.Char()
	per_street2 = fields.Char()
	per_zip = fields.Char(change_default=True)
	per_city = fields.Char()
	per_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
	per_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
	# medium = fields.Many2one('education.medium', string="Medium")
	# sec_lang = fields.Many2one('education.subject', string="Second language", required=True, domain=[('is_language', '=', True)])
	mother_tongue = fields.Many2one('education.mother.tongue', string="Mother Tongue", required=False)
	caste_id = fields.Many2one('religion.caste', string="Caste")
	religion_id = fields.Many2one('religion.religion', string="Religion")
	is_same_address = fields.Boolean(string="Is same Address?")
	nationality = fields.Many2one('res.country', string='Nationality', ondelete='restrict')
	application_id = fields.Many2one('education.application', string="Application No")
	class_history_ids = fields.One2many('education.class.history', 'student_id', string="Application No")
	#total_fees = fields.Float('student.fees.register', readonly=True,store=True)
	#paid_fees = fields.Float('student.fees.register',readonly=True,store=True)
	#due_fees = fields.Float('student.fees.register', readonly=True,store=True)
	doctor = fields.Char('Doctor Name', states={'done': [('readonly', True)]})
	designation = fields.Char('Designation')
	doctor_phone = fields.Char('Phone')
	# blood_group = fields.Char('Blood Group')
	height = fields.Float('Height', help="Hieght in C.M")
	weight = fields.Float('Weight', help="Weight in K.G")
	eye = fields.Boolean('Eyes')
	ear = fields.Boolean('Ears')
	nose_throat = fields.Boolean('Nose & Throat')
	respiratory = fields.Boolean('Respiratory')
	cardiovascular = fields.Boolean('Cardiovascular')
	neurological = fields.Boolean('Neurological')
	muskoskeletal = fields.Boolean('Musculoskeletal')
	dermatological = fields.Boolean('Dermatological')
	blood_pressure = fields.Boolean('Blood Pressure')
	comment = fields.Text()
	student_notes = fields.Text()
	emergency_calls = fields.Many2many('emergency.calls',string='Emergecny Calls')
	state  = fields.Selection([('not_registered','Not Registered'),('registered','Registered'),
								 ('transfer','Transfered'),('alumni','Alumni'),('pendent','Pendent'),('leave','leave')],
                           string='Status', required=True, default='not_registered',track_visibility='onchange')
	accessories_count = fields.Integer(string="accessories",store=True)
	transport_fee = fields.Float(string='Transportation Fees',readonly=True,store=True)
	# institution_fee = fields.Float(string='Institution Fees',readonly=True,store=True)
	guardian_relationship=fields.Selection([('father', 'Father'), ('mother', 'Mother'),
							  ('uncle', 'Uncle'), ('aunt', 'Aunt'),
							  ('kuncle', 'KUncle'), ('kaunt', 'KAunt'), ('brother', 'Brother'),
							  ('sister','Sister'),('grandfa','Grandfather'),('grandmo','Grandmother'),('other','Other')],
							 string='Guardian Relationship',track_visibility='onchange')
	student_sibling_ids = fields.Many2many('education.student','education_student_sibling_rel','student_id','sibling_id' ,string='Student Siblings', compute='compute_siblings')
	have_sibling = fields.Boolean(string='Have Sibling?')

	
	city_id = fields.Many2one("citeis.cities", string='Area')
	zone_id = fields.Many2one("zones.zones", string='Area')

	block = fields.Char(string='Block')
	home_no = fields.Char(string='Home No')
	sib_percentage = fields.Selection([('one', '10'), ('two', '15')],
							  string='Discount Percentage')
	
	admission_class_id = fields.Many2many('education.class', string='Class', required=True) ##### muneera
	
	# full_name=fields.Char(string='Student Full Name', compute='_compute_full_name') ##### muneera
    
	
	percentage = fields.Integer(string='Discount Percentage')
	previous_mark = fields.Float(string = 'درجة النجاح السابقه')

	# @api.depends('student_sibling_ids')
	# def _count_siblings(self):
	# 	siblings = self.env['education.student'].search_count([('id', 'in', self.student_sibling_ids.ids)])
	# 	self.siblings = siblings + 1

	_sql_constraints = [
		('ad_no', 'unique(ad_no)', "Another Student already exists with this admission number!"),
	]

	# @api.constrains('class_id')
	# def check_class_id(self):
	# 	for rec in self:
	# 		if self.class_id:
	# 			if rec.class_id.class_id.id != self.admission_class.id:
	# 				raise ValidationError(_('This divisionis not assigned to this Class '))
	# 			if rec.class_id.shool_id.id != self.school_id.id:
	# 				raise ValidationError(_('This divisionis not assigned to this school'))

	@api.constrains('phone')
	def _check_s_Phone(self):
		for rec in self:
		# raise ValidationError(rec)
			if rec.phone and len(rec.phone) != 10:
					raise ValidationError("يجب ان يتكون رقم الهاتف من عشره ارقام")
		



	@api.onchange('admission_class')
	def onchange_class_id(self):
		self.class_id = False
		domain = {'class_id': [('class_id', '=', self.admission_class.id),('gender', '=', self.gender),('school_id', '=', self.school_id)]}
		return {'domain': domain}

	@api.onchange('class_id')
	def onchange_class_division(self):
		for rec in self:
			if rec.class_id:
				if rec.class_id.student_count == rec.class_id.actual_strength:
					raise UserError(_('This class is fully, select another class or increace the class strength'))	
					rec.class_id = False
				if rec.class_id.school_id.id != self.school_id.id:
					raise ValidationError(_('This divisionis not assigned to this school'))
					rec.class_id = False
				if rec.class_id.class_id.id != self.admission_class.id :
					raise ValidationError(_('This divisionis not assigned to this Class '))
					rec.class_id = False
	
	@api.depends('parent_ids')
	def compute_siblings(self):
		for rec in self:
			sib_ids = self.env['education.student'].search([('parent_ids', '=', rec.parent_ids.id)])
			sibs_ids = []
			if rec.parent_ids:				
				for record in sib_ids:
					if record.id != rec.id:
					# if record.id != self.id:
						if record.state not in ['pendent','leave']:

							sibs_ids.append(record.id)
			rec.write({'student_sibling_ids':sibs_ids})

	# @api.onchange('parent_ids')
	# def onchange_parent_ids(self):
	# 	if self.parent_ids:
	# 		pa_ids = self.env['res.partner'].search([('name', '=', self.parent_ids.name)])

	# 		self.parent_id = self.parent_ids.parttner_id.id
	# 	else:
	# 		self.parent_id = False

	#@api.multi
	def action_view_invoice(self):
		'''
		This function returns an action that
		display existing invoices of given student ids and show a invoice"
		'''
		result = self.env.ref('education_fee.action_fee_tree1')
		id = result and result.id or False
		result = self.env['ir.actions.act_window'].browse(id).read()[0]
		inv_ids = []
		academic_year=self.env['education.academic.year'].search([('current_year','=',True)])
		for student in self:
			inv_ids += [invoice.id for invoice in student.invoice_ids]
			result['context'] = {'default_partner_id': student.partner_id.id}
		invoice_list = self.env['account.invoice'].search_count([('student_id','=',self.id),('academic_year_id','=',academic_year.id),('is_institution_fee','=',True)])

		if len(inv_ids) > 0 and invoice_list>0:
			result['domain'] = \
				"[('id','in',[" + ','.join(map(str, inv_ids)) + "]),('is_institution_fee','=',True)]"
		else:
			res = self.env.ref('education_fee.receipt_form')
			result['views'] = [(res and res.id or False, 'form')]
			result['res_id'] = False and inv_ids[0] or False
			result['context'] = {'default_student_id':self.id,'default_class_division_id':self.class_id.id,'default_is_institution_fee':True}
		return result
		
	#@api.multi
	def create_transportation_fee_invoice(self):
		'''
		This function returns an action that
		display existing invoices of given student ids and show a invoice"
		'''
		result = self.env.ref('education_fee.action_fee_tree1')
		id = result and result.id or False
		result = self.env['ir.actions.act_window'].browse(id).read()[0]
		inv_ids = []
		academic_year=self.env['education.academic.year'].search([('current_year','=',True)])
		invoice_list = self.env['account.invoice'].search_count([('student_id','=',self.id),('academic_year_id','=',academic_year.id),
																  ('is_Tansportation_fee','=',True)])
		for student in self:
			inv_ids += [invoice.id for invoice in student.invoice_ids]
			result['context'] = {'default_partner_id': student.partner_id.id,'default_is_Tansportation_fee':True}
		if len(inv_ids) > 0 and invoice_list>0:
			result['domain'] = \
				"[('id','in',[" + ','.join(map(str, inv_ids)) + "]),('is_Tansportation_fee','=',True)]"
		else:

			res = self.env.ref('education_fee.receipt_form')
			result['views'] = [(res and res.id or False, 'form')]
			result['res_id'] =  False
			result['context'] = {'default_student_id':self.id,'default_class_division_id':self.class_id.id,'default_is_Tansportation_fee':True}
		return result


	#@api.multi
	def stock_deivery_order(self):
		year = self.env['education.academic.year'].search([('current_year', '=', True)])
		payslip_id = self.env['student.fees.register'].search([('student_id','=',self.id),('academic_year','=',year.id)])
		acc = payslip_id.mapped('accessory_ids')
		if len(acc)>0:
			res  = self.env['stock.picking'].create({
					'partner_id':self.partner_id.id,
					'picking_type_id':self.env['stock.picking.type'].search([('code', '=', 'outgoing'),('warehouse_id.company_id','=',self.school_id.company_id.id)], limit=1).id,
					'location_id':self.env['stock.location'].search([('usage', '=', 'internal'),('company_id','=',self.school_id.company_id.id)], limit=1).id,
					'location_dest_id':self.env['stock.location'].search([('usage', '=', 'view'),('company_id','=',self.school_id.company_id.id)], limit=1).id,
					'move_type':'one',
				})
			for rec in acc:
				mov = self.env['stock.move'].create({
					'picking_id':res.id,
					'product_id':rec.accessoryType.id,
					'product_uom_qty':rec.quantity,
					'product_uom':1,
					'location_id':res.location_id.id,
					'location_dest_id':res.location_dest_id.id,
					'name':res.name,

					})
			for student in self:
				student.accessories_count = self.env[
					'stock.picking'].search_count(
					[('partner_id', '=', student.partner_id.id)])
		else:
			raise UserError(_('There are no specific accessories'))	

	# #@api.multi
	# def Update_student(self):
	# 	student = self.env['education.student'].search([])
	# 	for rec in student:
	# 		for x in rec.partner_id:
	# 			if x.is_student==False:
	# 				x.is_student=True
	#@api.multi
	def Update_student(self):
		# student = self.env['education.student'].search([('admission_class','=',1)])
		student = self.env['education.student'].search([('admission_class','=',1)])
		for rec in student:
			if self.per_street2 and self.mobile:
				res = self.env['emergency.calls'].create({'name':self.per_street2,'phone':self.mobile})
				self.emergency_calls = [(4,res.id)]
			elif self.per_street and self.phone:
				res = self.env['emergency.calls'].create({'name':self.per_street,'phone':self.phone})
				self.emergency_calls = [(4,res.id)]
			# for x in rec.partner_id:
			# 	if x.is_student==False:
			# 		x.is_student=True


