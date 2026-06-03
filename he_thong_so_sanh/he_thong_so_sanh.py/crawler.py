import sqlite3
import os

def khoi_tao_database():
    print("🔄 Đang khởi tạo và nạp dữ liệu vào Database...")
    
    # Kết nối tới file dữ liệu SQLite (Tự động tạo file nếu chưa có)
    conn = sqlite3.connect('so_sanh_gia.db')
    cursor = conn.cursor()

    # XÓA BẢNG CŨ (Nếu có) để cập nhật danh sách iPhone mới không bị trùng lặp dữ liệu cũ
    cursor.execute("DROP TABLE IF EXISTS san_pham")

    # TẠO BẢNG MỚI với cấu trúc chuẩn: tên, giá, sàn, link, ảnh
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS san_pham (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ten TEXT NOT NULL,
            gia TEXT NOT NULL,
            san TEXT NOT NULL,
            link TEXT NOT NULL,
            anh TEXT NOT NULL
        )
    ''')

    # -------------------------------------------------------------
    # DANH SÁCH DỮ LIỆU IPHONE ĐẦY ĐỦ ĐỂ TEST TÌM KIẾM VÀ BỘ LỌC
    # -------------------------------------------------------------
    data_thu_thap_duoc = [
        # --- NHÓM GIÁ DƯỚI 10 TRIỆU ---
        ("Apple iPhone 11 64GB Chính hãng VN/A", "8.990.000 đ", "Shopee", "https://shopee.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"),
        ("iPhone 11 128GB (Hàng cũ 99%)", "7.500.000 đ", "Lazada", "https://lazada.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"),

        # --- NHÓM GIÁ TỪ 10 ĐẾN 20 TRIỆU ---
        ("iPhone 13 128GB VN/A", "13.490.000 đ", "Tiki", "https://tiki.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"),
        ("Apple iPhone 14 128GB Đen", "16.890.000 đ", "Shopee", "https://shopee.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"),
        ("Điện thoại Apple iPhone 15 128GB", "19.790.000 đ", "Lazada", "https://lazada.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"),

        # --- NHÓM GIÁ TRÊN 20 TRIỆU ---
        ("Apple iPhone 15 Pro 128GB đầy đủ màu", "24.690.000 đ", "Tiki", "https://tiki.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"),
        ("iPhone 15 Pro Max 256GB Chính hãng VN/A", "29.490.000 đ", "Shopee", "https://shopee.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"),
        ("iPhone 15 Pro Max 512GB Titan tự nhiên", "34.990.000 đ", "Lazada", "https://lazada.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150")
    ]

    # Thực hiện lệnh ghi dữ liệu hàng loạt vào cơ sở dữ liệu
    cursor.executemany('''
        INSERT INTO san_pham (ten, gia, san, link, anh) 
        VALUES (?, ?, ?, ?, ?)
    ''', data_thu_thap_duoc)

    # Lưu lại thay đổi và đóng file database
    conn.commit()
    conn.close()
    
    print("🎉 Hoàn thành! Đã nạp thành công 8 sản phẩm iPhone cực chuẩn vào file so_sanh_gia.db!")

if __name__ == '__main__':
    khoi_tao_database()