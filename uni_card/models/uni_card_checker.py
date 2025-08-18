from odoo import models,fields,api
from pyzbar.pyzbar import decode
from pdf2image import convert_from_bytes

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

    @api.onchange('card')
    def _onchange_code(self):
        """
        Triggered whenever the PDF file is changed.
        Converts the first page of the PDF to an image,
        decodes the QR code from the image,
        then checks if a student (uni.student) exists
        with ref = decoded value.
        If found → is_valid = True, else False.
        """
        if not self.card:
            self.is_valid = False
            self.status=""
            self.name=""
            self.gender=""
            self.academic_year=""
            self.department=""
            self.image=False

            return

        try:
            # Convert PDF (binary) to images
            pages = convert_from_bytes(self.card)
            if not pages:
                self.is_valid = False
                self.status=""
                self.name=""
                self.gender=""
                self.academic_year=""
                self.department=""
                self.image=False

                return

            # Decode QR from the first page
            decoded_list = decode(pages[0])
            if not decoded_list:
                self.is_valid = False
                self.status=""
                self.name=""
                self.gender=""
                self.academic_year=""
                self.d
                self.gender=""
                self.academic_year=""
                self.department=""
                self.image=Falseepartment=""
                self.image=False

                return

            qr_value = decoded_list[0].data.decode('utf-8')
            qr_value=qr_value.split('_')

            # Search for the student
            student = self.env['uni.student'].search([('ref', '=', qr_value[0])])
            
            if student:
                self.is_valid = True
                self.status="IS VALID!"
                self.name=student.name
                self.gender=student.gender
                self.academic_year=student.academic_year
                self.department=student.department
                self.image=student.image
            
            if not student:
                self.is_valid=False
                self.status=""
                self.name=""
                self.gender=""
                self.academic_year=""
                self.department=""
                self.image=False


        except Exception:
            # Any error → mark as not valid
            self.is_valid = False
            self.status=""
            self.name=""
            self.gender=""
            self.academic_year=""
            self.department=""
            self.image=False