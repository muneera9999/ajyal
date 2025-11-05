from odoo import models, fields


class EducationEpisode(models.Model):
    _name = 'education.episode'
    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    class_ids = fields.One2many('education.class','episode_id',string='Classes',domain=[('episode_id','=',False)])


class EducationClass(models.Model):
    _inherit = 'education.class'

    episode_id = fields.Many2one('education.episode',string='Episode')