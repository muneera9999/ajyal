from odoo import http
from odoo import models
from ast import literal_eval
from odoo.http import request
from xlsxwriter import workbook
import io
import xlsxwriter

class XlsxStudentReport(http.Controller):
    @http.route('/student/excel/report/<string:student_ids>', type="http", auth="user")
# class XlsxStudentReport(models.Model):
#    workbook.save("C:\Users\munee\OneDrive\Desktop\Areez\excel-files/student_report.xlsx")
    
    def download_student_excel_report(self,student_ids):    

        student_ids_list = literal_eval(student_ids)
        student_ids = request.env['education.student'].browse(student_ids_list)

        ## student_ids= request.env['student'].browse(literal_eval(student_ids))
        print(student_ids)
        output=io.BytesIO()
        workbook= xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet= workbook.add_worksheet('Students')
        header_format= workbook.add_format({'bold': True, 'bg_color':"#4B4BF9", 'border':1, 'align':'center'})
        string_format= workbook.add_format({'border':1, 'align':'center'})
        date_format = workbook.add_format({'border': 1, 'align': 'center', 'num_format': 'yyyy-mm-dd'})
        
        # student_model= request.env['student']
        # field_mapping= [('','')]

        headers =['Name','Admission Class','Admission Number','Gender','Academic year']
        
        for col_num,header in enumerate(headers):
           worksheet.write(0,col_num, header, header_format)

        # student = 'education.student'
        row_num=1   
        for student in student_ids:
            
            worksheet.write(row_num,0, student.partner_id.name, string_format)
            worksheet.write(row_num,1, student.admission_class.name, string_format)
            worksheet.write(row_num,2, student.ad_no, string_format)
            worksheet.write(row_num,3, student.gender, string_format)
            worksheet.write(row_num,4, student.academic_year_id.name, date_format)
            # worksheet.write(row_num,6, student.faculty_id.name, string_format)
            
            row_num += 1


        workbook.close()
        output.seek(0)

        file_name='StudentReport.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}')]
        )