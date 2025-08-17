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
    study_year=fields.Char(compute='_compute_study_date')
    start_date=fields.Date(string='Date Issued')
    end_date=fields.Date(string='Expire Date')
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

    @api.depends('start_date','end_date')
    def _compute_study_date(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.study_year=f"{rec.start_date.year } - {rec.end_date.year}"
            else:
                rec.study_year=""





# from io import BytesIO
# import base64
# try:
#     import qrcode
# except ImportError:
#     qrcode = None

# class UniStudentCard(models.Model):
#     _name = 'uni.student.card'

#     student_id = fields.Many2one('uni.student')
#     barcode = fields.Binary("QR Code", compute="_compute_qr_code")

#     @api.depends('student_id')
#     def _compute_qr_code(self):
#         """
#         Generate a QR code (image) containing basic student info.
#         """
#         for rec in self:
#             if not (qrcode and base64) or not rec.student_id:
#                 rec.barcode = False
#                 continue

#             qr = qrcode.QRCode(
#                 version=1,
#                 error_correction=qrcode.constants.ERROR_CORRECT_L,
#                 box_size=3,
#                 border=4,
#             )
#             # Add whatever data you want to appear in the QR code
#             qr.add_data(f"ID : {rec.student_id.ref}")
#             qr.add_data(f", Name : {rec.student_id.name}")
#             qr.add_data(f", Department : {rec.student_id.department}")
#             qr.make(fit=True)

#             img = qr.make_image()
#             buffer = BytesIO()
#             img.save(buffer, format='PNG')
#             rec.barcode = base64.b64encode(buffer.getvalue())