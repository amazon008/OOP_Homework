from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# -------------------------------------------------------------------------
# HÀM TRUY VẤN VÀ LỌC DỮ LIỆU
# -------------------------------------------------------------------------
def tim_kiem_trong_database(keyword, san_chon, muc_gia):
    if not keyword:
        return []
    
    if not os.path.exists('so_sanh_gia.db'):
        print("CẢNH BÁO: Không tìm thấy file so_sanh_gia.db. Vui lòng chạy file crawler.py!")
        return []

    conn = sqlite3.connect('so_sanh_gia.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    # Lấy toàn bộ sản phẩm khớp từ khóa
    sql_query = "SELECT * FROM san_pham WHERE ten LIKE ?"
    cursor.execute(sql_query, ('%' + keyword + '%',))
    ket_qua = cursor.fetchall()
    conn.close()
    
    # --- BẮT ĐẦU XỬ LÝ LỌC DỮ LIỆU BẰNG PYTHON ---
    ket_qua_da_loc = []
    
    for row in ket_qua:
        sp = dict(row)
        
        # 1. Lọc theo nền tảng (Shopee, Lazada, Tiki)
        # Nếu người dùng có chọn sàn, và sàn của sản phẩm KHÔNG nằm trong danh sách chọn -> Bỏ qua
        if san_chon and sp['san'].lower() not in [s.lower() for s in san_chon]:
            continue
            
        # 2. Lọc theo mức giá
        if muc_gia:
            # Chuyển "29.490.000 đ" -> Thành số nguyên 29490000 để so sánh
            gia_str = sp['gia'].replace('.', '').replace(' đ', '').replace('đ', '').replace(',', '').strip()
            try:
                gia_int = int(gia_str)
            except ValueError:
                gia_int = 0 # Tránh lỗi web nếu giá bị sai định dạng
                
            # Kiểm tra các điều kiện giá
            if muc_gia == 'duoi10' and gia_int >= 10000000:
                continue
            if muc_gia == '10den20' and (gia_int < 10000000 or gia_int > 20000000):
                continue
            if muc_gia == 'tren20' and gia_int <= 20000000:
                continue
                
        # Nếu qua được hết các bộ lọc trên thì đưa vào danh sách hiển thị
        ket_qua_da_loc.append(sp)
        
    return ket_qua_da_loc

# -------------------------------------------------------------------------
# CẤU HÌNH ĐỊNH TUYẾN FLASK (ROUTES)
# -------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '').strip()
    
    # Lấy danh sách các sàn được tick (Checkbox trả về dạng list)
    san_chon = request.args.getlist('san') 
    
    # Lấy mức giá được chọn (Radio button trả về 1 value)
    muc_gia = request.args.get('gia', '') 
    
    # Truyền thêm tham số lọc vào hàm
    ket_qua_tim_kiem = tim_kiem_trong_database(keyword, san_chon, muc_gia)
    
    # Trả các biến về HTML để form ghi nhớ trạng thái người dùng đã chọn
    return render_template('index.html', 
                           keyword=keyword, 
                           results=ket_qua_tim_kiem,
                           san_chon=san_chon,
                           muc_gia=muc_gia)

if __name__ == '__main__':
    app.run(debug=True)