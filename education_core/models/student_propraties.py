"""






"""
from dateutil import relativedelta
from odoo import models, fields

class StudentPropreties(models.Model):
	_name = 'student.properties'


	descripption = fields.Text(string='behavior')
	student_id = fields.Many2one('education.student',string="Student Name") 
	teacher = fields.Many2one('education.faculty',string='Teacher')
	date = fields.Date(string='Date')
