import pytesseract
from pdf2image import convert_from_path

# ระบุเส้นทางไปยัง tesseract.exe ที่ติดตั้งในเครื่อง
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
import os
from pdf2image import convert_from_path
import pytesseract

# กำหนดเส้นทางไปยัง Tesseract (ปรับเปลี่ยน path ตามที่ติดตั้งในเครื่องของคุณ เช่น C:/Program Files/Tesseract-OCR/tesseract.exe)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pdf_path = "คำชี้แจงประกอบงบประมาณ 2570.pdf"
output_txt = "คำชี้แจงประกอบงบประมาณ_2570_OCR_ครบถ้วน.txt"

print("กำลังแปลงหน้า PDF เป็นรูปภาพ...")
# แปลงทุกหน้าของ PDF เป็นรูปภาพ (สามารถกำหนด dpi เช่น 300 เพื่อความคมชัดในการอ่าน OCR)
images = convert_from_path(pdf_path, dpi=300)
total_pages = len(images)
print(f"แปลงสำเร็จ จำนวนทั้งหมด {total_pages} หน้า เริ่มกระบวนการ OCR...")

with open(output_txt, "w", encoding="utf-8") as f:
    for i, image in enumerate(images):
        page_num = i + 1
        print(f"กำลังประมวลผล OCR หน้าที่ {page_num}/{total_pages}...")       
        # ใช้ OCR อ่านภาษาไทย ('tha') และอังกฤษ ('eng')
        text = pytesseract.image_to_string(image, lang='tha+eng')
        
        f.write(f"--- หน้า {page_num}/{total_pages} ---\n")
        f.write(text.strip() + "\n\n")

print(f"แปลงข้อความทั้งหมดเสร็จสิ้น บันทึกไฟล์ที่: {output_txt}")