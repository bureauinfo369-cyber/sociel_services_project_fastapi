from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
import arabic_reshaper
from reportlab.lib.enums import TA_RIGHT
from bidi.algorithm import get_display
import io
import os
from datetime import datetime
from num2words import num2words
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import subprocess
def reshape_arabic(text):
    """Reshape and reorder Arabic text for proper display."""
    if isinstance(text, str):
        return get_display(arabic_reshaper.reshape(text))
    return str(text)

def Demande_de_prêt(file_path, demande_data, emp_data):
    # Set page size
    width, height = A4
    
    # Register DejaVu Sans font (installed in Dockerfile)
    font_name = "Helvetica"  # Default fallback
    
    dejavu_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    dejavu_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    if os.path.exists(dejavu_regular):
        try:
            # Register regular font
            pdfmetrics.registerFont(TTFont("DejaVuSans", dejavu_regular))
            print(f"✓ Registered DejaVuSans from: {dejavu_regular}")
            
            # Register bold font (use regular as fallback if bold not found)
            if os.path.exists(dejavu_bold):
                pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", dejavu_bold))
                print(f"✓ Registered DejaVuSans-Bold from: {dejavu_bold}")
            else:
                pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", dejavu_regular))
                print(f"⚠ Bold not found, using regular as bold")
            
            # Register the complete font family
            registerFontFamily(
                'DejaVuSans',
                normal='DejaVuSans',
                bold='DejaVuSans-Bold',
                italic='DejaVuSans',
                boldItalic='DejaVuSans-Bold'
            )
            
            font_name = "DejaVuSans"
            print(f"✓ Successfully registered DejaVuSans font family")
            
        except Exception as e:
            print(f"✗ Failed to register DejaVu font: {e}")
            print(f"✓ Falling back to Helvetica (limited Arabic support)")
    else:
        print(f"✗ DejaVu font not found at: {dejavu_regular}")
        print(f"✓ Using Helvetica (limited Arabic support)")
    
    print(f"Using font: {font_name}")
    
    # Create temporary filename
    temp_filename = f"{file_path}.temp"
    
    # Create the document
    doc = SimpleDocTemplate(
        temp_filename, 
        pagesize=A4, 
        rightMargin=20, 
        leftMargin=20, 
        topMargin=20, 
        bottomMargin=50
    )
    
    # Create styles - ALL using font_name variable
    styles = getSampleStyleSheet()
    
    arabic_title = ParagraphStyle(
        'ArabicTitle',
        parent=styles['Normal'],  # Changed from Title to Normal
        fontName=font_name,
        fontSize=20,
        alignment=1,  # center
        spaceAfter=20,
        leading=28
    )
    
    arabic_header = ParagraphStyle(
        'ArabicHeader',
        parent=styles['Normal'],  # Changed from Heading1 to Normal
        fontName=font_name,
        fontSize=18,
        alignment=2,  # right
        spaceAfter=4,
        leading=24
    )
    
    arabic_header_info = ParagraphStyle(
        'ArabicHeaderInfo',
        parent=styles['Normal'],  # Changed from Heading1 to Normal
        fontName=font_name,
        fontSize=14,
        alignment=2,  # right
        spaceAfter=10,
        leading=18
    )
    arabic_header_info.alignment = TA_RIGHT
    arabic_normal = ParagraphStyle(
        'ArabicNormal',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=16,
        alignment=1,  # right
        spaceAfter=2,
        leading=24
    )
    
    # Content elements
    content = []
    
    # Add Header
    content.append(Paragraph(reshape_arabic("الجمهورية الجزائرية الديمقراطية الشعبية"), arabic_title))
    content.append(Spacer(1, 2))
    
    content.append(Paragraph(reshape_arabic("وزارة المالية"), arabic_header))
    content.append(Paragraph(reshape_arabic("المديرية العامة للمحاسبة"), arabic_header))
    content.append(Paragraph(reshape_arabic("المديرية الجهوية للخزينة غرداية"), arabic_header))
    content.append(Paragraph(reshape_arabic("لجنة الخدمات الإجتماعية لعمال"), arabic_header))
    content.append(Paragraph(reshape_arabic("خزينة الولاية و خزائن بلديات تمنراست"), arabic_header))
    content.append(Spacer(1, 10))

    # Add date
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_paragraph = Paragraph(reshape_arabic(f" تمنراست في : {current_date}"), arabic_header_info)
    content.append(Spacer(1, 5))
    content.append(date_paragraph)
    
    # Employee information
    content.append(Paragraph(reshape_arabic(f"اللقب و الإسم :  {emp_data.Nom}"), arabic_header_info))
    content.append(Paragraph(reshape_arabic(f"الرتبة أو الوظيفة : {emp_data.Poste}"), arabic_header_info))
    content.append(Paragraph(reshape_arabic(f"الإقامة الإدارية : {emp_data.residence_admin}"), arabic_header_info))
    # Report title
    report_title = "طلب منحة ختان"
    content.append(Paragraph(reshape_arabic(report_title), arabic_title))
    content.append(Spacer(20, 5))
    
    # Employee information
    content.append(Paragraph(reshape_arabic(f'اتقدم الى سيادتكم بطلبي هذا و المتمثل في طلب منحة الختان للطفل '), arabic_normal))
    content.append(Paragraph(reshape_arabic(f'({emp_data.Nom}) التي تمنحها اللجنة.'), arabic_normal))
    content.append(Paragraph(reshape_arabic(f"و في الأخير تقبلو مني فائق الاحترام و التقدير"), arabic_normal))
    content.append(Spacer(1, 20))
    content.append(Paragraph(reshape_arabic(f"تاريخ الطلب : {demande_data.Début_Déduction}"), arabic_header_info))
    content.append(Paragraph(reshape_arabic(f"رقم حساب المعني : {emp_data.NumCompte}"), arabic_header_info))
    content.append(Paragraph(reshape_arabic(f"المرفقات : "), arabic_header_info))
    content.append(Paragraph(reshape_arabic("إمضاء المعني  "), arabic_header_info))
    content.append(Spacer(1, 10))
    
    # Page number function - uses font_name
    def add_page_number(canvas_obj, doc_obj):
        canvas_obj.saveState()
        page_num = canvas_obj.getPageNumber()
        text = f"Page {page_num}"
        canvas_obj.setFont(font_name, 9)
        canvas_obj.drawRightString(doc_obj.pagesize[0] - 20, 20, text)
        canvas_obj.restoreState()
    
    # Build the initial document
    doc.build(content, onFirstPage=add_page_number, onLaterPages=add_page_number)
    
    # Modify PDF to add treasury secretary signature on last page
    from PyPDF2 import PdfReader, PdfWriter
    
    reader = PdfReader(temp_filename)
    writer = PdfWriter()
    
    for page_num, page in enumerate(reader.pages):
        writer.add_page(page)
        
        if page_num == len(reader.pages) - 1:  # Last page
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            
            packet = io.BytesIO()
            signature_canvas = canvas.Canvas(packet, pagesize=(width, height))
            
            footer_text = reshape_arabic("أمين الخزينة")
            signature_canvas.setFont(font_name, 10)
            signature_canvas.drawRightString(width - 50, 60, footer_text)
            
            signature_canvas.save()
            packet.seek(0)
            
            signature_pdf = PdfReader(packet)
            page.merge_page(signature_pdf.pages[0])
    
    # Write final output
    with open(file_path, 'wb') as output_file:
        writer.write(output_file)
    
    # Delete temporary file
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
    
    print(f"✓ PDF created successfully: {file_path}")

def convert_to_arabic_dinars_and_centimes(amount):
    try:
        if isinstance(amount, str):
            amount = amount.replace(',', '').replace(' ', '')
        
        amount = float(amount)
        
        if amount < 0:
            return "لا يمكن تحويل الأرقام السالبة"
        
        whole = int(amount)
        decimal_part = round((amount - whole) * 100)
        
        if whole == 0:
            whole_words = "صفر دينار"
        else:
            whole_words = num2words(whole, to='currency', lang='ar')
            whole_words = whole_words.replace("ريال", "دينار جزائري")
            if "دينار" not in whole_words:
                if whole == 1:
                    whole_words += " دينار"
                elif whole == 2:
                    whole_words += " ديناران"  
                elif 3 <= whole <= 10:
                    whole_words += " دنانير"
                else:
                    whole_words += " دينار"
        
        if decimal_part == 0:
            return whole_words
        
        centimes_words = num2words(decimal_part, to='cardinal', lang='ar')
        
        if decimal_part == 1:
            centimes_words += " سنتيم"
        elif decimal_part == 2:
            centimes_words += " سنتيمان"
        elif 3 <= decimal_part <= 10:
            centimes_words += " سنتيمات"
        else:
            centimes_words += " سنتيم"
        
        return f"{whole_words} و {centimes_words}"
        
    except ValueError:
        return "خطأ: يجب إدخال رقم صحيح"
    except ImportError:
        return "خطأ: مكتبة num2words غير مثبتة"
    except Exception as e:
        return f"خطأ غير متوقع: {str(e)}"
    


def generate_demande_pdf_type_khitan(demande_data, employee_data, output_dir="print", subdirs=None):
    """Generate a demande PDF with flexible path management."""
    if subdirs:
        full_path = os.path.join(output_dir, *subdirs)
    else:
        full_path = output_dir
    
    os.makedirs(full_path, exist_ok=True)
    
    pdf_filename = f"demande_{demande_data.demande_id}.pdf"
    pdf_file_path = os.path.join(full_path, pdf_filename)
    
    Demande_de_prêt(pdf_file_path, demande_data, employee_data)
    
    print(f"✓ PDF saved to: {pdf_file_path}")

    # Open the PDF file
    #"linux"
    subprocess.call(["xdg-open", pdf_file_path])
    
    
        
    return pdf_file_path

# Example usage with sample data
if __name__ == "__main__":
    # Sample data - replace with your database data
    account_number = "4002-000"
    report_date = "نوفمبر / 2024"
    
    # Sample data - This would come from your database
    # Format: [رقم, الجهة المساهمة, المبلغ]
    sample_data = []
    
    # Generate sample data to demonstrate pagination
    for i in range(1, 50):  # Generate 100 rows to test multiple pages
        sample_data.append([
            i*10000,  # المبلغ
            f"جهة مستفيدة {i}",  # الجهة المساهمة
           
            i   # الرقم
        ])
    
    # Create and save the PDF
    pdf_file_path = "LOG.pdf"
    Demande_de_prêt(pdf_file_path, account_number, report_date, sample_data)
    print(f"PDF saved as: {pdf_file_path}")
