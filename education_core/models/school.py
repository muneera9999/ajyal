# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

# import time
import re
import calendar
from datetime import datetime
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
	DEFAULT_SERVER_DATETIME_FORMAT
# from odoo.exceptions import except_orm
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class SchoolSchool(models.Model):
	''' Defining School Information '''
	_name = 'school.school'
	_inherits = {'res.company': 'company_id'}
	_description = 'School Information'
	# _rec_name = "com_name"

	@api.model
	def _lang_get(self):
		'''Method to get language'''
		languages = self.env['res.lang'].search([])
		return [(language.code, language.name) for language in languages]

	company_id = fields.Many2one('res.company', 'Company',
								 ondelete="cascade",
								 required=True)
	# com_name = fields.Char('School Name',related='company_id.name',
 #                           store=True)
	code = fields.Char('Code', required=True)
	class_id = fields.One2many('education.class', 'school_id',
								'Class')
	gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('mix', 'Mix')],
							  string='Gender')
	lang = fields.Selection(_lang_get, 'Language',
							help='''If the selected language is loaded in the
								system, all documents related to this partner
								will be printed in this language.
								If not, it will be English.''')



class usersinherit(models.Model):

	_inherit = 'res.users'	

	class_id = fields.Many2many('education.class.division', string='Class')
	subject_id = fields.Many2many('education.subject', string='Subject')

class cities(models.Model):
	_description = "Cities"
	_name = 'citeis.cities'


	country_id = fields.Many2one('res.country', string='Country')
	name = fields.Char(string='State Name', required=True)


class zone(models.Model):
	_description = "Zones"
	_name = 'zones.zones'


	country_id = fields.Many2one('res.country', string='Country')
	name = fields.Char(string='State Name', required=True)
