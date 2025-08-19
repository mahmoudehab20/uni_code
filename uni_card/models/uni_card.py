from odoo import models,fields,api
from io import BytesIO
import base64
try:
    import qrcode
except ImportError:
    qrcode = None

class UniCard(models.Model):
    _name='uni.card'

    student_id=fields.Many2one('uni.student')
    ref=fields.Char(string='ID',readonly=True,related='student_id.ref')
    name=fields.Char(related='student_id.name')
    department=fields.Selection([
        ('is','IS'),
        ('it','IT'),
        ('cs','CS'),
    ],related='student_id.department')
    academic_year=fields.Selection([
        ('first','First'),
        ('second','Second'),
        ('third','Third'),
        ('fourth','Fourth')
    ],related='student_id.academic_year')
    image=fields.Binary(related='student_id.image')
    study_year=fields.Char(related='student_id.study_year')
    start_date=fields.Date(string='Date Issued',related='student_id.start_date')
    end_date=fields.Date(string='Expire Date',related='student_id.end_date')
    barcode = fields.Binary("QR Code", compute='_compute_qr_code')

    @api.depends('student_id')
    def _compute_qr_code(self):
        for rec in self:
            if not rec.student_id or not qrcode:
                rec.barcode = False
                continue

            data = f"{rec.ref}_{rec.name[:3]}_{rec.end_date}"
            img = qrcode.make(data)
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            rec.barcode = base64.b64encode(buffer.getvalue())

            if rec.barcode:
                rec.student_id.state='valid'

   