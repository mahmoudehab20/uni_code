from odoo import models,fields,api
import random

class UniStudent(models.Model):
    _name='uni.student'

    
    state=fields.Selection([
        ('draft','Draft'),
        ('valid','Valid'),
        ('expired','Expired')
    ],default='draft')
    ref=fields.Char(default='new',string='ID',readonly=True)
    name=fields.Char()
    department=fields.Selection([
        ('is','IS'),
        ('it','IT'),
        ('cs','CS'),
    ])
    academic_year=fields.Selection([
        ('first','First'),
        ('second','Second'),
        ('third','Third'),
        ('fourth','Fourth')
    ])
    image=fields.Binary()
    gender=fields.Selection([
        ('m','Male'),
        ('f','Female')
    ])
    study_year=fields.Char(compute='_compute_study_date')
    start_date=fields.Date(string='Date Issued')
    end_date=fields.Date(string='Expire Date')

    @api.depends('start_date','end_date')
    def _compute_study_date(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.study_year=f"{rec.start_date.year } - {rec.end_date.year}"
            else:
                rec.study_year=""


    def create(self,vals):
        res = super().create(vals)
        sequnce=self.env['ir.sequence'].search([('id','=',self.env.ref('uni_card.student_sequence').id)])
        prefix=''
        # set security number for department
        if res.department == 'is':
            prefix+='1'
        elif res.department == 'it':
            prefix+='2'
        elif res.department == 'cs':
            prefix+='3'

        if res.gender == 'm':
            prefix+=str(random.choice([1,3,5,7,9]))
        
        if res.gender == 'f':
            prefix+=str(random.choice([2,4,6,8]))

        if res.academic_year == 'first':
            prefix+='4'
        elif res.academic_year == 'second':
            prefix+='5'
        elif res.academic_year == 'third':
            prefix+='6'
        elif res.academic_year == 'fourth':
            prefix+='7'
        
        sequnce.prefix=prefix
        res.ref=self.env['ir.sequence'].next_by_code('students_seq')

        return res