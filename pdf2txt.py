import pypdf

# 1. กำหนดชื่อไฟล์ PDF ต้นทางและไฟล์ .txt ปลายทาง
pdf_path = "คำชี้แจงประกอบงบประมาณ 2570.pdf"
txt_output_path = "คำชี้แจงประกอบงบประมาณ_2570_ทุกหน้า.txt"

# 2. โหลดไฟล์ PDF และตรวจสอบจำนวนหน้าทั้งหมด
reader = pypdf.PdfReader(pdf_path)
total_pages = len(reader.pages)
print(f"จำนวนหน้าทั้งหมดใน PDF: {total_pages}")

# 3. วนลูปอ่านข้อความทีละหน้าและบันทึกลงในไฟล์ .txt
with open(txt_output_path, "w", encoding="utf-8") as f:
    for page_num in range(total_pages):
        page = reader.pages[page_num]
        text = page.extract_text()
        
        # เขียนหัวข้อกำกับแต่ละหน้าเพื่อความเป็นระเบียบ
        f.write(f"--- หน้า {page_num + 1}/{total_pages} ---\n")
        if text:
            f.write(text + "\n\n")

print(f"ส่งออกข้อความทั้งหมดสำเร็จ บันทึกที่ไฟล์: {txt_output_path}")