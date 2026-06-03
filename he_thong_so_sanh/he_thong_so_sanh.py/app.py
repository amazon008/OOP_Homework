from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# -------------------------------------------------------------------------
# HÀM TRUY VẤN DATABASE (MÔ HÌNH LƯU TRỮ TỐI ƯU)
# -------------------------------------------------------------------------
def tim_kiem_trong_database(keyword):
    # Nếu người dùng không nhập gì mà ấn tìm kiếm thì trả về mảng rỗng
    if not keyword:
        return []
    
    # Kiểm tra an toàn: Nếu chưa có file DB (chưa chạy crawler.py) thì dừng lại
    if not os.path.exists('so_sanh_gia.db'):
        print("CẢNH BÁO: Không tìm thấy file so_sanh_gia.db. Vui lòng chạy file crawler.py trước để tạo DB!")
        return []

    # Mở kết nối tới Database SQLite
    conn = sqlite3.connect('so_sanh_gia.db')
    
    # Ép kiểu dữ liệu trả về thành Dictionary để dễ dàng gọi {{ sp.ten }}, {{ sp.gia }} trên HTML
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    # Câu lệnh SQL: Tìm kiếm các sản phẩm có tên chứa từ khóa
    # Ký tự '%' đại diện cho bất kỳ chuỗi nào (Tìm kiếm tương đối)
    sql_query = "SELECT * FROM san_pham WHERE ten LIKE ?"
    
    cursor.execute(sql_query, ('%' + keyword + '%',))
    ket_qua = cursor.fetchall()
    
    # Đóng kết nối để giải phóng tài nguyên
    conn.close()
    
    return ket_qua

# -------------------------------------------------------------------------
# CẤU HÌNH ĐỊNH TUYẾN FLASK (ROUTES)
# -------------------------------------------------------------------------

# 1. TRANG CHỦ: Hiển thị giao diện tìm kiếm ban đầu
@app.route('/')
def home():
    return render_template('index.html')

# 2. TRANG KẾT QUẢ TÌM KIẾM
@app.route('/search', methods=['GET'])
def search():
    # Lấy từ khóa người dùng nhập từ ô <input name="keyword">, xoá khoảng trắng thừa ở 2 đầu
    keyword = request.args.get('keyword', '').strip()
    
    # Truy vấn dữ liệu siêu tốc từ Database
    ket_qua_tim_kiem = tim_kiem_trong_database(keyword)
    
    # Render ra trang index.html kèm theo từ khóa và kết quả tìm được
    return render_template('index.html', keyword=keyword, results=ket_qua_tim_kiem)

if __name__ == '__main__':
    # Chạy ứng dụng dưới Local
    app.run(debug=True)