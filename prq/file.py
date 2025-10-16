#file{file_json , file_csv , file_excel , file_to_excel , pdf_report}
'''
Reading file and making dataframe
خواندن فایل و ساخت دیتافریم
انواع فایل های داده:
    json , csv , excel
'''
'''
Reading json file
خواندن فایل جیسون
'''
def file_json(file='' , s_index=int()): #ساخت تابع فایل json
    from pandas import DataFrame  , read_json
    from numpy import arange
    filein = read_json(file,) #خواندن فایل
    df = DataFrame(filein , index=arange(s_index , len(filein))) #ساخت دیتافریم و نرمال کردن ایندکس
    return df #برگرداندن دیتا فریم
'''
file_json(file , s_index) -> file: نام فایل ورودی , s_index: ایندکس شروع
'''
#*********************************************************************************
'''
Reading csv file
خواندن فایل سی اس وی
'''
def file_csv(file='' , s_index=int()): #ساخت تابع فایل csv
    from pandas import DataFrame  , read_csv
    from numpy import arange
    filein = read_csv(file,) #خواندن فایل
    df = DataFrame(filein , index=arange(s_index , len(filein))) #ساخت دیتافریم و نرمال کردن ایندکس
    return df #برگرداندن دیتا فریم
'''
file_csv(file , s_index) -> file: نام فایل ورودی , s_index: ایندکس شروع
'''
#*********************************************************************************
'''
Reading Excel file
خواندن فایل اکسل
'''
def file_excel(file='' , s_index=int()): #ساخت تابع فایل excel/xlsx
    from pandas import DataFrame  , read_excel
    from numpy import arange
    filein = read_excel(file,) #خواندن فایل
    df = DataFrame(filein , index=arange(s_index , len(filein))) #ساخت دیتافریم و نرمال کردن ایندکس
    return df #برگرداندن دیتا فریم
'''
file_excel(file , s_index) -> file: نام فایل ورودی , s_index: ایندکس شروع
'''
#*********************************************************************************
'''
Saving in an xlsx file
ذخیره در فایل اکسل
'''
def file_to_excel(df , filename): #ساختن تابع اکسل
    import pandas as pd
    with pd.ExcelWriter(filename, engine='openpyxl') as writer: #نوشتن فایل اکسل
        df.to_excel(writer, sheet_name='Sheet1', index=False) #ایندکس فالز باشه شماره ردیف نوشته نمیشه
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        for column_cells in worksheet.columns: #تنظیم اندازه سلول ها
            max_length = 0
            column = column_cells[0].column_letter
            for cell in column_cells:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column].width = adjusted_width
'''
file_to_excel( df , filename) -> df : دیتافریم مدنظر , filename : نام فایل ذخیره ای
'''
#*********************************************************************************
'''
Creating a PDF report
ساخت گزارش در فایل پی دی اف
'''
def pdf_report(filename, content, font_farsi_path, font_english_path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    from bidi.algorithm import get_display
    import arabic_reshaper
    from PIL import Image
    import os
    def reshape_text(text):  # پشتیبانی از حروف فارسی
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    def is_farsi(text):  # تشخیص فارسی بودن متن
        return any('\u0600' <= ch <= '\u06FF' for ch in text)
    def draw_page_border(c, width, height, margin=30):  # کادر دور
        r = int("AD", 16) / 255
        g = int("D8", 16) / 255
        b = int("E6", 16) / 255
        c.setStrokeColorRGB(r, g, b)
        c.setLineWidth(1)
        x = margin
        y = margin
        rect_width = width - 2 * margin
        rect_height = height - 2 * margin
        c.rect(x, y, rect_width, rect_height, fill=0, stroke=1)
    def wrap_text(text, font_name, font_size, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + (' ' if current_line else '') + word
            text_width = pdfmetrics.stringWidth(test_line, font_name, font_size)
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 40
    y_position = height - 60
    pdfmetrics.registerFont(TTFont('Vazir', font_farsi_path))
    pdfmetrics.registerFont(TTFont('Arial', font_english_path))
    draw_page_border(c, width, height, margin)
    for item in content:
        if item[0] == 'text':
            text = item[1]
            font_size = 14
            max_text_width = width - 2 * margin - 20
            if is_farsi(text):
                text = reshape_text(text)
                lines = wrap_text(text, 'Vazir', font_size, max_text_width)
                c.setFont('Vazir', font_size)
                for line in lines:
                    text_width = pdfmetrics.stringWidth(line, 'Vazir', font_size)
                    x_position = width - margin - text_width - 10#راست‌چین
                    c.drawString(x_position, y_position, line)
                    y_position -= 25
                    if y_position < 100:
                        c.showPage()
                        draw_page_border(c, width, height, margin)
                        y_position = height - 60
            else:
                lines = wrap_text(text, 'Arial', font_size, max_text_width)
                c.setFont('Arial', font_size)
                for line in lines:
                    x_position = margin + 10  # چپ‌چین
                    c.drawString(x_position, y_position, line)
                    y_position -= 25
                    if y_position < 100:
                        c.showPage()
                        draw_page_border(c, width, height, margin)
                        y_position = height - 60
        elif item[0] == 'image':
            img_path = item[1]
            img_title = item[2]
            if not os.path.exists(img_path):
                continue
            img = Image.open(img_path)
            img_width, img_height = img.size
            max_width = width - 2 * margin - 40
            max_height = 200
            ratio = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            if y_position - new_height < 100:
                c.showPage()
                draw_page_border(c, width, height, margin)
                y_position = height - 60
            x_img = (width - new_width) / 2
            y_img = y_position - new_height
            c.drawImage(img_path, x_img, y_img, width=new_width, height=new_height)
            font_size = 12
            y_text = y_img - 25
            if is_farsi(img_title):
                shaped_title = reshape_text(img_title)
                c.setFont('Vazir', font_size)
                text_width = pdfmetrics.stringWidth(shaped_title, 'Vazir', font_size)
                x_text = (width - text_width) / 2
                c.drawString(x_text, y_text, shaped_title)
            else:
                c.setFont('Arial', font_size)
                text_width = pdfmetrics.stringWidth(img_title, 'Arial', font_size)
                x_text = (width - text_width) / 2
                c.drawString(x_text, y_text, img_title)
            y_position = y_text - 30
    c.save()
    print(f"PDF saved as {filename}")
'''
pdf_report(filename , content , fontfa , fonteng) -> filename: نام فایل ذخیره ای , content: محتویات مدنظر , fontfa & fonteng: فونت فارسی و انگلیسی
'''
#*********************************************************************************
'''
Github: https://github.com/ahkiyani
Linkedin: https://www.linkedin.com/in/amirhossein-kiyani1381
G-mail: https://amirho3einkiyani.2002@gmail.com
'''
