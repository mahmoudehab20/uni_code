from odoo import models,fields,api
import base64
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode

class UniCardChecker(models.Model):
    _name='uni.card.checker'

    card=fields.Binary()
    status=fields.Char()
    name=fields.Char()
    gender=fields.Char()
    department=fields.Char()
    academic_year=fields.Char()
    image=fields.Image()
    is_valid=fields.Boolean(default=True)

    # @api.depends('card')
    # def check_card(self):
    #     for rec in self:
    #         if not rec.card:
    #             rec.status=""
    #             return True

    #         # decode QR image
    #         print(rec.card,"card@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #         img_data = base64.b64decode(rec.card)
    #         img = Image.open(BytesIO(img_data))
    #         decoded = decode(img)
    #         if decoded:
    #             qr_data = decoded[0].data.decode("utf-8")
    #             print(qr_data,"qr_data@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #             # Example: search the order by the QR code content
    #             qr_data=qr_data.split('_')
    #             student_id=rec.env['uni.student'].search([('ref','=',qr_data[0])])
    #             if not student_id:
    #                 rec.status='Not Valid!'
    #                 rec.is_valid=False

    #             if student_id.state == 'valid':
    #                 rec.name=student_id.name
    #                 rec.gender=student_id.gender
    #                 rec.department=student_id.department
    #                 rec.academic_year=student_id.academic_year
    #                 rec.image=student_id.image
    #                 rec.status='Valid!'
    #                 rec.is_valid=True
