from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import arabic_reshaper
from reportlab.pdfgen import canvas
from bidi.algorithm import get_display
import io
import os
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime  # Import datetime module
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
#pdfmetrics.registerFont(TTFont('Amiri', '/path/to/your/font/Amiri-Regular.ttf'))  # Adjust the path accordingly
#pdfmetrics.registerFont(TTFont('Amiri', 'Amiri-Regular.ttf'))  # Ensure you have the font file in your directory
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import arabic_reshaper
from bidi.algorithm import get_display

#
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import arabic_reshaper
from bidi.algorithm import get_display




def reshape_arabic(text):
    """Reshape and reorder Arabic text for proper display."""
    if isinstance(text, str):
        return get_display(arabic_reshaper.reshape(text))
    return str(text)

def RIEMP_Print(file_path, account_number, report_date, table_data):
    """
    Create a PDF that looks like the Algerian treasury document with data from database.
    
    Args:
        file_path: Path to save the PDF file
        account_number: The account number to display
        report_date: The report date (month/year)
        table_data: List of rows with data from database, where each row is a list/tuple with 4 elements:
                    [رقم, الجهة المسددة, الجهة المستفيدة, المبلغ]
    """
    # Set page size to landscape A4
    width, height = landscape(A4)  # This is the key change - Using landscape orientation
    
    # Register a font that supports Arabic characters
    pdfmetrics.registerFont(TTFont("Arial", "Arial.ttf"))
    
    # Create the document with landscape orientation
    doc = SimpleDocTemplate(file_path, pagesize=landscape(A4), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=50)
    
    # Create styles
    styles = getSampleStyleSheet()
    arabic_title = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Title'],
        fontName='Arial',
        fontSize=16,
        alignment=1,  # center
        spaceAfter=6
    )
    
    arabic_header = ParagraphStyle(
        'ArabicHeader',
        parent=styles['Heading1'],
        fontName='Arial',
        fontSize=14,
        alignment=2,  # right
        spaceAfter=2
    )
    
    arabic_normal = ParagraphStyle(
        'ArabicNormal',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=12,
        alignment=2,  # right
        spaceAfter=2
    )
    arabic_left = ParagraphStyle(
        'ArabicNormal',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=14,
        alignment=0,  # right
        spaceAfter=2
    )
    # Content elements to be added to the document
    content = []
    
    # Add Header
    content.append(Paragraph(reshape_arabic("الجمهورية الجزائرية الديمقراطية الشعبية"), arabic_title))
    content.append(Spacer(1, 2))
    
    # Header text
    content.append(Paragraph(reshape_arabic("وزارة المالية"), arabic_header))
    content.append(Paragraph(reshape_arabic("المديرية العامة للمحاسبة"), arabic_header))
    content.append(Paragraph(reshape_arabic("المديرية الجهوية للخزينة غرداية"), arabic_header))
    content.append(Paragraph(reshape_arabic("خزينة ولاية تمنراست"), arabic_header))
    content.append(Paragraph(reshape_arabic("الرقم ....... / ت ج ر/ .......20"), arabic_header))
   
   # At the point where you prepare your content, add the printing date
    current_date = datetime.now().strftime("%Y-%m-%d")  # Format the date as needed
    date_paragraph = Paragraph(reshape_arabic(f" تمنراست في : {''}"), arabic_normal)

    # Append the date paragraph to the content
    content.append(Spacer(1, 10))  # Add some space before the date
    content.append(date_paragraph)
    
    content.append(Paragraph(reshape_arabic("يشرفني أن أوضح لكم في الجدول أدناه المبالغ المرجعة من أجل  تمكيننا من تسوية هذه المبالغ  أرجو منكم إعادة هذا البيان مكتملا و موقعا من قبلكم مع إرفاق إشعار"), arabic_header))
                               
    content.append(Paragraph(reshape_arabic(" بالدفع و بيان الدفع جديدين بالمعطيات الصحيحة و في حالة تغير إسم الستفيد يجب إرفاق شهادة إدارية"), arabic_header))
    
    content.append(Spacer(1, 10))
    #content.append(Paragraph(reshape_arabic(" رد الأمر بالصرف "), arabic_header))
     # Report title
    report_title = f" إعادة الإدراج"
    
    content.append(Paragraph(reshape_arabic(report_title), arabic_title))
    content.append(Spacer(1,8))
    Riemp = f" مديرية : "
    content.append(Paragraph(reshape_arabic(Riemp), arabic_title))
    content.append(Spacer(1, 3))
    content.append(Paragraph(reshape_arabic("  رد الأمر بالصرف : إعادة إدراج في الجدول أدناه الإسم الكامل و رقم الحساب الصحيحين للمستفيد   "), arabic_left))
    content.append(Paragraph(reshape_arabic("     بشكل واضح "), arabic_title))
   

   # left_align_header = ParagraphStyle( name='LeftAlign',fontName='Amiri', fontSize=12, alignment=2)  # 1 corresponds to left alignment
    #content.append(Paragraph(reshape_arabic(" نص جديد على اليسار "), arabic_header))
  
    

   
    
    # Account number - adjusted width for landscape
    account_table_data = [[
        reshape_arabic(account_number),  # Left side (value)
        reshape_arabic("الحساب :")       # Right side (label)
    ]]
    
    account_table = Table(account_table_data, colWidths=[550, 100])  # Adjusted width for landscape
    account_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),   # Left align the value
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Right align the label
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    content.append(account_table)
    content.append(Spacer(1, 15))
    # Report title
    arabic_left = ParagraphStyle(
        'ArabicNormal',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=12,
        alignment=0,  # left
        spaceAfter=2
        
    )
    
    
    # Prepare table headers
    table_headers = [
        reshape_arabic("الحساب"),
        reshape_arabic("الإسم"),
        reshape_arabic("الرقم"),
        reshape_arabic("المبلغ"),
        reshape_arabic("مكان العمل"),
        reshape_arabic("الإسم و اللقب  "),
        reshape_arabic("الرقم")
    ]
    
    # Calculate column widths - adjusted for landscape
    available_width = width - 40  # Total width minus margins
    col_widths = [
        available_width * 0.15,
        available_width * 0.10,  # الجهة المسددة - 25%
        available_width * 0.05,   # الرقم - 10%
        available_width * 0.10,  # الجهة المستفيدة - 25%
        available_width * 0.15,  # الجهة المسددة - 25%
        available_width * 0.20,   # وضع اليد  - 15%
        available_width * 0.05    # الرقم - 10%
    ]
    
    # Create table data with headers
    page_table_data = [table_headers]
    
    # Initialize total amount
    total_amount = 0

    # Add all data rows at once
    for row in table_data:
        formatted_row = []
        for cell in row:
            # Ensure numbers are right-aligned and accumulate total
            if isinstance(cell, (int, float)):
                formatted_row.append(f"{cell:,.2f}")  # Format numbers with commas and two decimal places
                total_amount += cell  # Accumulate total amount
            else:
                formatted_row.append(reshape_arabic(str(cell)))
        page_table_data.append(formatted_row)

    # Round total_amount to 2 decimal places
    total_amount = round(total_amount, 2)
    
    # Create the table with style
    table = Table(page_table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'RIGHT'),  # Right-align the amount column
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    content.append(table)
    
    # Add total amount below the table
  
    total_paragraph = Paragraph(
    reshape_arabic(f"الإجمالي: {total_amount:,.2f}"),
    arabic_normal
)
    content.append(Spacer(1, 25))
    content.append(total_paragraph)

    signature_table_data = [[
        reshape_arabic(f"الأمر بالصرف"),  # Left side (value)
        reshape_arabic(f" أمين الخزينة")       # Right side (label)
    ]]
    
    signature_table = Table(signature_table_data, colWidths=[550, 100])  # Adjusted width for landscape
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Left align the value
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Right align the label
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(Spacer(1, 40))
    content.append(signature_table)
    

    # Define a simple page function for page numbers
    def add_page_number(canvas, doc):
        canvas.saveState()
        page_num = canvas.getPageNumber()
        text = f"page {page_num}"
        canvas.setFont("Arial", 9)
        canvas.drawRightString(doc.pagesize[0] - 20, 20, text)
        canvas.restoreState()

    # Build the document with page numbers
    doc.build(content, onFirstPage=add_page_number, onLaterPages=add_page_number)

    # Now add the treasury secretary signature on the last page
    reader = PdfReader(file_path)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        writer.add_page(page)
        
        # If this is the last page, add the treasury secretary signature
        if page_num == len(reader.pages) - 1:  # Last page
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            
            # Create a separate canvas just for the signature
            packet = io.BytesIO()
            signature_canvas = canvas.Canvas(packet, pagesize=(width, height))
            
            # Add the treasury secretary signature
            footer_text = reshape_arabic("أمين الخزينة")
            signature_canvas.setFont("Arial", 10)
            signature_canvas.drawRightString(width - 40, 20, footer_text)
            
            # Save the canvas
            signature_canvas.save()
            
            # Move to the beginning of the buffer
            packet.seek(0)
            
            # Create a new PDF with the signature
            signature_pdf = PdfReader(packet)
            
            # Add the signature to the last page
            page.merge_page(signature_pdf.pages[0])

    # Write the output to the final file
    with open(file_path, 'wb') as output_file:
        writer.write(output_file)

# Example usage with sample data
if __name__ == "__main__":
    account_number = "4002-000"
    report_date = "نوفمبر / 2024"
    
    # Sample data
    sample_data = []
    for i in range(1, 53):  # Generate 52 rows
        sample_data.append([
            f" الحساب  {i}",
            f" الإسم  {i}",
            i,  # الرقم
            i * 10000,  #  المبلغ
            f"2025",  # الجهة المسددة
            f" الإسم  {i}",   # وضع اليد
            i   # الرقم
        ])
    
    # Create and save the PDF
    pdf_file_path = "RIEMP.pdf"
    RIEMP_Print(pdf_file_path, account_number, report_date, sample_data)
    print(f"PDF saved as: {pdf_file_path}")