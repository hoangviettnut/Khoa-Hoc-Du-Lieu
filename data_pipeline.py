import pandas as pd
import numpy as np

def process_exam_data(input_path, output_path):
    print("⏳ 1. Đang tải dữ liệu thô vào Pandas...")
    # Vì cột ban đầu tên là 'Student ID', ta đọc nó dưới dạng string để không mất số 0
    df = pd.read_csv(input_path, dtype={'Student ID': str})

    print("🔄 2. Đổi tên cột từ Tiếng Anh sang Tiếng Việt...")
    # Tạo từ điển map tên cột cho khớp với file Kaggle của bạn
    column_mapping = {
        'Student ID': 'sbd',
        'Mathematics': 'toan',
        'Literature': 'ngu_van',
        'Foreign language': 'ngoai_ngu',
        'Physics': 'vat_li',
        'Chemistry': 'hoa_hoc',
        'Biology': 'sinh_hoc',
        'History': 'lich_su',
        'Geography': 'dia_li',
        'Civic education': 'gdcd'
    }
    # Tiến hành đổi tên cột
    df = df.rename(columns=column_mapping)

    print("🧹 3. Làm sạch Số báo danh và trích xuất Mã tỉnh...")
    df['sbd'] = df['sbd'].str.strip()
    df['sbd'] = df['sbd'].str.zfill(8) # Đảm bảo đủ 8 số
    df['ma_tinh'] = df['sbd'].str[:2]  # Lấy 2 số đầu làm mã tỉnh

    print("📊 4. Chuẩn hóa điểm số và xử lý NaN...")
    mon_thi = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_li', 'hoa_hoc', 
               'sinh_hoc', 'lich_su', 'dia_li', 'gdcd']
    
    for mon in mon_thi:
        if mon in df.columns:
            df[mon] = pd.to_numeric(df[mon], errors='coerce')

    # Xóa các dòng không có bất kỳ điểm thi nào
    df = df.dropna(subset=mon_thi, how='all')

    print("🚨 5. Nhận diện điểm liệt (<= 1.0)...")
    df['diem_liet'] = (df[mon_thi] <= 1.0).any(axis=1)

    print("💾 6. Đang xuất file dữ liệu sạch...")
    # Reorder lại cột cho đẹp: sbd, ma_tinh, rồi đến các điểm, và diem_liet ở cuối
    cols_order = ['sbd', 'ma_tinh'] + mon_thi + ['diem_liet']
    df = df[cols_order]
    
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ HOÀN TẤT! Đã lưu file dữ liệu sạch tại: {output_path}")

# --- Khởi chạy luồng xử lý ---
if __name__ == "__main__":
    RAW_FILE = 'diem_thi_thpt_2023_raw.csv'
    CLEAN_FILE = 'diem_thi_thpt_2023_clean.csv'
    
    process_exam_data(RAW_FILE, CLEAN_FILE)