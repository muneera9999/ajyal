from odoo import models,fields
class DbExpireCrone(models.Model):
   _name = 'db.epire.cron'

   def cron_demo_method(self):

       # acadimicYear_id= self.env['education.academic.year'].search([('current_year','=',True)])

       
       # cur_date = datetime.today()
       # new_date = cur_date + timedelta(days=90)