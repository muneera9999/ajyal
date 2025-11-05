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


class EducationSubject(models.Model):
    _name = 'education.subject'

    name = fields.Char(string='Subject Name', required=True, help="Name of the Subject")
    is_language = fields.Boolean(string="Language", help="Tick if this subject is a language")
    is_lab = fields.Boolean(string="Lab", help="Tick if this subject is a Lab")
    code = fields.Char(string="Code", help="Enter the Subject Code")
    type = fields.Selection([('compulsory', 'Compulsory'), ('elective', 'Elective')],
                            string='Type', default="compulsory",
                            help="Choose the type of the subject")
    weightage = fields.Float(string='Weightage', help="Enter the weightage for this subject")
    description = fields.Text(string='Description')
    class_id = fields.Many2many('education.class',string='Class Name')

    _sql_constraints = [
        ('code', 'unique(code)', "Another Subject already exists with this code!"),
    ]

    # @api.constrains('weightage')
    # def check_weightage(self):
    #     """return warning if the weightage given is not a possitive value"""
    #     for rec in self:
    #         if rec.weightage <= 0:
    #             raise ValidationError(_('Weightage must be Possitive'))


class StandardMedium(models.Model):
    _name = "education.medium"
    _description = "Standard Medium"

    name = fields.Char(string='Name', required=True,
                       help="Enter the Name of the Medium")
    code = fields.Char(string='Code', help="Enter the Medium Code")
    description = fields.Text(string='Description')


class EducationMotherTongue(models.Model):
    _name = "education.mother.tongue"
    _description = "Mother Tongue Language"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')


class EducationSyllabus(models.Model):
    _name = 'education.syllabus'


    # @api.model
    @api.model_create_multi

    def create(self, vals_list):
        """Return the name as a str of class + division"""
        # res = super(EducationClassDivision, self).create(vals)
        for vals in vals_list:

            class_id = self.env['education.class'].browse(vals['class_id'])
           


        # class_id = self.env['education.class'].browse(vals['class_id'])
            subject_id = self.env['education.subject'].browse(vals['subject_id'])
        # subject_id = self.env['education.subject'].browse(vals['subject_id'])
            name = str(subject_id.name + '-' + class_id.name)
            vals['name'] = name
        return super(EducationSyllabus, self).create(vals_list)
        

    @api.depends('class_id','subject_id')
    def _update_name(self):
        """Return the name as a str of class + division"""
        for rec in self:

            if rec.subject_id and rec.class_id:
                rec.name = str(str(rec.subject_id.name) + '-' + str(rec.class_id.name))     

    no = fields.Char(string='No',default="1")

    name = fields.Char('Syllabus Name', required=True,compute='_update_name' ,store=True )
    class_id = fields.Many2one('education.class', string='Class')
    subject_id = fields.Many2one('education.subject', string='Subject')
    total_lectures = fields.Float(string='Total Lectues')
    description = fields.Text(string='Syllabus Modules')

    # @api.constrains('total_hours')
    # def validate_time(self):
    #     """returns validation error if the hours is not a possitive value"""
    #     for rec in self:
    #         if rec.total_hours <= 0:
    #             raise ValidationError(_('Hours must be greater than Zero'))
