import json
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db


def convert_excel_to_firebase_json(excel_path, json_output_path):
  # อ่านไฟล์ Excel ข้อมูลงบประมาณ ปี 2570
  df = pd.read_excel(excel_path, sheet_name=0, skiprows=5, header=None)
  df.columns = ['col0', 'col1', 'col2', 'col3']

  current_plan = 'แผนงานบริหารงานทั่วไป'
  current_job = 'งานบริหารทั่วไป'
  current_group = 'งบบุคลากร'

  projects_dict = {}
  item_counter = 1

  # วนลูปอ่านข้อมูลทุกบรรทัดในไฟล์ Excel
  for idx, row in df.iterrows():
    c0 = str(row['col0']).strip() if pd.notna(row['col0']) else ''
    c1 = str(row['col1']).strip() if pd.notna(row['col1']) else ''
    c3 = str(row['col3']).strip() if pd.notna(row['col3']) else ''

    text = c1 if c1 else c0

    # จัดหมวดหมู่ตามโครงสร้างระเบียบงบประมาณทางราชการ
    if text.startswith('แผนงาน'):
      current_plan = text
      continue
    elif text.startswith('งาน'):
      current_job = text
      continue
    elif text.startswith('งบ'):
      current_group = text
      continue

    # ตรวจสอบและดึงตัวเลขงบประมาณปี 2570
    if c3 != '' and c3 != 'ปี 2570' and c3 != 'nan':
      try:
        amount = float(c3.replace(',', ''))

        # กรองเฉพาะรายการย่อยที่ไม่ใช่แถบยอดรวมสรุป (รวม...)
        if not text.startswith('รวม'):
          prj_id = f'PRJ-2570-{item_counter:03d}'
          projects_dict[prj_id] = {
              'project_name': text,
              'plan': current_plan,
              'job': current_job,
              'budget_group': current_group,
              'department': current_plan.replace('แผนงาน', 'สำนัก/กอง'),
              'initial_budget': amount,
              'current_budget': amount,
              'status': 'APPROVED',
              'pinned_by_executive': False,
              'note': f'{current_plan} -> {current_job} -> {current_group}',
          }
          item_counter += 1
      except ValueError:
        pass

  # โครงสร้าง JSON ที่พร้อม Import เข้า Firebase Realtime Database
  firebase_data = {
      'organization': 'องค์การบริหารส่วนตำบลข่วงเปา',
      'district': 'อำเภอจอมทอง จังหวัดเชียงใหม่',
      'fiscal_year': 2570,
      'total_projects': len(projects_dict),
      'projects': projects_dict,
      'executive_notebook_settings': {
          'pinned_widgets': ['PRJ-2570-001', 'PRJ-2570-002', 'PRJ-2570-003']
      },
  }

  # บันทึกออกเป็นไฟล์ JSON
  with open(json_output_path, 'w', encoding='utf-8') as f:
    json.dump(firebase_data, f, ensure_ascii=False, indent=4)

  print(
      f'✅ แปลงข้อมูลสำเร็จครบถ้วนทั้งหมด {len(projects_dict)} รายการ ลงไฟล์'
      f' {json_output_path}'
  )


# เรียกใช้งาน
if __name__ == '__main__':
  convert_excel_to_firebase_json(
      'ข้อมูลงบประมาณ ปี 2570.xlsx', 'budget_2570_full.json'
  )