import sqlite3

# 1. HÀM TẠO DATABASE VÀ BẢNG LƯU TRỮ
def khoi_tao_database():
    # Sẽ tự động tạo ra file so_sanh_gia.db trong thư mục của bạn
    conn = sqlite3.connect('so_sanh_gia.db')
    cursor = conn.cursor()

    # Tạo bảng chứa dữ liệu sản phẩm
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
    conn.commit()
    return conn

# 2. HÀM CHẠY CÀO DỮ LIỆU VÀ LƯU VÀO KHO
def chay_tool_cao_du_lieu():
    conn = khoi_tao_database()
    cursor = conn.cursor()

    # Xóa dữ liệu cũ (tùy chọn) để cập nhật giá mới mỗi ngày
    cursor.execute('DELETE FROM san_pham')

    print("Đang tiến hành cào dữ liệu (Mô phỏng)...")
    
    # -------------------------------------------------------------
    # SAU NÀY BẠN SẼ VIẾT CODE CÀO THẬT BẰNG SELENIUM/BEAUTIFULSOUP Ở ĐÂY.
    # HIỆN TẠI MÌNH BƠM DATA MẪU VÀO DATABASE ĐỂ WEB CÓ CÁI HIỂN THỊ.
    # -------------------------------------------------------------
    data_thu_thap_duoc = [
        ("iPhone 15 Pro Max 256GB Chính hãng VN/A", "29.490.000 đ", "Shopee", "https://shopee.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"),
        ("Điện thoại Apple iPhone 15 128GB", "19.790.000 đ", "Lazada", "https://lazada.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"),
        ("Apple iPhone 15 Pro 128GB đầy đủ màu", "24.690.000 đ", "Tiki", "https://tiki.vn", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150")
    ]

    # Insert toàn bộ data cào được vào Database
    cursor.executemany('''
        INSERT INTO san_pham (ten, gia, san, link, anh)
        VALUES (?, ?, ?, ?, ?)
    ''', data_thu_thap_duoc)

    conn.commit()
    print(f"Đã lưu thành công {len(data_thu_thap_duoc)} sản phẩm vào Database!")
    conn.close()

if __name__ == '__main__':
    # Khi chạy file này, nó sẽ tạo DB và nạp dữ liệu
    chay_tool_cao_du_lieu()