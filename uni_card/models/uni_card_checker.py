from odoo import models,fields,api
from pdf2image import convert_from_bytes
from pyzbar.pyzbar import decode  
import base64


class UniCardChecker(models.Model):
    _name='uni.card.checker'

    card=fields.Binary()
    status=fields.Char(store=True)
    name=fields.Char()
    gender=fields.Char()
    department=fields.Char()
    academic_year=fields.Char()
    image=fields.Image()
    is_valid=fields.Boolean(default=True)


    @api.onchange('card')
    def _compute_status(self):
           # Assuming 'self' is a recordset of your model
        for record in self:
            if record.card:
                
                # Decode the binary data
                pdf_data = base64.b64decode(record.card)
                pages=convert_from_bytes(pdf_data)

                for page in pages:
                    qr_codes = decode(page)
                    for qr in qr_codes:
                        student_id=self.env['uni.student'].search([('ref','=',str(qr.data)[2:].split('_')[0])])
                        gender_label = dict(student_id._fields['gender'].selection).get(student_id.gender)
                        department_label=dict(student_id._fields['department'].selection).get(student_id.department)
                        year_label=dict(student_id._fields['academic_year'].selection).get(student_id.academic_year)

                        if student_id.state == 'valid':
                            record.status="Valid"
                            record.is_valid=True
                            record.name=student_id.name
                            record.image=student_id.image
                            record.academic_year=year_label
                            record.department=department_label
                            record.gender=gender_label


                        elif student_id.state == 'draft':
                            record.status="Valid But Has No ID!"
                            record.is_valid=False
                            record.name=student_id.name
                            record.image=student_id.image
                            record.academic_year=year_label
                            record.department=department_label
                            record.gender=gender_label


                        elif student_id.state == 'expired':
                            record.status="Expired!"
                            record.is_valid=False
                            record.name=student_id.name
                            record.image=student_id.image
                            record.academic_year=year_label
                            record.department=department_label
                            record.gender=gender_label


            else:
                record.status='not valid'
                record.is_valid=False
                record.name=""
                record.department=""
                record.academic_year=""
                record.image=False
                record.gender=""