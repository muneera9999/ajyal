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

from odoo import fields, models, api

class EducationFaculty(models.Model):
    _name = 'education.faculty'
    _inherit = ['mail.thread']
    _description = 'Faculty Record'

    #@api.multi
    def create_employee(self):
        """Creating the employee for the faculty"""
        for rec in self:
            teacher_job = self.env['hr.job'].search([('is_teacher', '=', True)])

            values = {
                # 'name': rec.name +"\t"+ rec.second_name+"\t"+ rec.middle_name+"\t"+rec.last_name,
                'name': rec.name,

                'gender': rec.gender,
                'birthday': rec.date_of_birth,
                # 'image': rec.image,
                'work_phone': rec.phone,
                'job_id': teacher_job.id,
                'work_email': rec.email,
            }
            emp_id = self.env['hr.employee'].create(values)
            rec.employee_id = emp_id.id

    def create_partner(self):
        """Creating the employee for the faculty"""
        for rec in self:
            values = {
                'name': rec.name,
                
                'company_type': 'person',
                'mobile': rec.phone,
                'phone': rec.mobile,
                
            }
            part_id = self.env['res.partner'].create(values)
            rec.partner_id = part_id.id

    # @api.model_create_multi
    # @api.model
    def create(self, vals):
        """Over riding the create method to assign
        the sequence for newly creating records"""
        vals['faculty_id'] = self.env['ir.sequence'].next_by_code('education.faculty')
        res = super(EducationFaculty, self).create(vals)
        return res

    name = fields.Char(string='Name', required=True, help="Enter the first name")
    faculty_id = fields.Char(string="ID", readonly=True)
    second_name = fields.Char(string='Second Name', help="Enter Second name")
    middle_name = fields.Char(string='Middle Name', help="Enter Middle name")
    last_name = fields.Char(string='Last Name', help="Enter the last name")
    image = fields.Binary(string="Image")
    email = fields.Char(string="Email", help="Enter the Email for contact purpose")
    phone = fields.Char(string="Phone", help="Enter the Phone for contact purpose")
    mobile = fields.Char(string="Mobile", help="Enter the Mobile for contact purpose")
    date_of_birth = fields.Date(string="Date Of birth", help="Enter the DOB")
    date_of_hire = fields.Date(string="Date Of Hire", help="Enter the DOB")
    Social_status = fields.Selection([('married', 'Married'), ('single', 'Single'), ('divorced', 'Divorced'),
        ('widower', 'Widower')], string='Social Status')

    contract_type = fields.Selection([('employee', 'Employee'), ('contract', 'Contract')], string="Contract Type", 
        default='employee')
    partner_id = fields.Many2one('res.partner', string="Related partner")

    lectures_number = fields.Char(string="Lectures Number") 
    preperation = fields.Boolean(string='preperation') 
    qualification = fields.Selection([('university', 'University'), ('master', 'Master'), ('divorced', 'Divorced'),
        ('phd', 'PHD')], string='Qualification')
    guardian_name = fields.Char(string="Guardian", help="Your guardian is ")
    father_name = fields.Char(string="Father", help="Your Father name is ")
    mother_name = fields.Char(string="Mother", help="Your Mother name is ")
    subject_lines = fields.Many2many('education.subject', string='Subject Lines')
    classes = fields.Many2many('education.class', string='Classes')
    employee_id = fields.Many2one('hr.employee', string="Related Employee")
    degree = fields.Many2one('hr.recruitment.degree', string="Degree", Help="Select your Highest degree")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string='Gender', required=True, default='male', track_visibility='onchange')
    blood_group = fields.Selection([('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'), ('o-', 'O-'),
                                    ('ab-', 'AB-'), ('ab+', 'AB+')],
                                   string='Blood Group',  default='a+', track_visibility='onchange')
  

    fuculty_attachment_id = fields.Many2many('ir.attachment', 'teacher_attachment_rel', 'doc_id', 'attach_id3', string="Attachment",
                                         help='You can attach the copy of your document', copy=False)


class fucultyAttachment(models.Model):
    _inherit = 'ir.attachment'

    teacher_attachment_rel = fields.Many2many('education.faculty', 'fuculty_attachment_id', 'attach_id3', 'doc_id',
                                      string="Attachment", invisible=1)

class Jobs(models.Model):
    _inherit = 'hr.job'
 
    is_teacher = fields.Boolean(string='Is teacher', default=False)


class Jobs(models.Model):
    _inherit = 'hr.employee'

    is_teacher = fields.Boolean(string='Is assistant', related="job_id.is_teacher")
