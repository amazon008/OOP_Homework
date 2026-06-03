from flask import Flask, render_template, request

app = Flask(__name__)

# -------------------------------------------------------------------------
# LOGIC CÀO DỮ LIỆU / SO SÁNH GIÁ (GIẢ LẬP)
# Bro có thể giữ nguyên hoặc tích hợp hàm cào (Scraper) thực tế của bro vào đây
# -------------------------------------------------------------------------
def cao_du_lieu_so_sanh(keyword):
    # Đây là danh sách dữ liệu mẫu để web hiển thị khi tìm kiếm.
    # Khi bro chạy code cào thật từ Shopee/Lazada, cấu trúc trả về nên tương tự thế này:
    if not keyword:
        return []
        
    keyword_lower = keyword.lower()
    data_mau = [
        {
            "ten": "iPhone 15 Pro Max 256GB Chính hãng VN/A",
            "gia": "29.490.000 đ",
            "san": "Shopee",
            "link": "https://shopee.vn",
            "anh": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"
        },
        {
            "ten": "Điện thoại Apple iPhone 15 128GB",
            "gia": "19.790.000 đ",
            "san": "Lazada",
            "link": "https://lazada.vn",
            "anh": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"
        },
        {
            "ten": "Apple iPhone 15 Pro 128GB đầy đủ màu",
            "gia": "24.690.000 đ",
            "san": "Tiki",
            "link": "https://tiki.vn",
            "anh": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=150"
        }
    ]
    
    # Lọc các sản phẩm mẫu có chứa từ khóa người dùng tìm kiếm
    ket_qua = [sp for sp in data_mau if keyword_lower in sp["ten"].lower()]
    return ket_qua


# -------------------------------------------------------------------------
# CẤU HÌNH ĐỊNH TUYẾN FLASK (ROUTES)
# -------------------------------------------------------------------------

# 1. TRANG CHỦ: Hiển thị giao diện tìm kiếm ban đầu
@app.route('/')
def home():
    return render_template('index.html')


# 2. TRANG KẾT QUẢ: Khớp chính xác với action="/search" method="GET" từ index.html
@app.route('/search', methods=['GET'])
def search():
    # Lấy từ khóa người dùng nhập từ ô <input name="keyword">
    keyword = request.args.get('keyword', '')
    
    # Gọi hàm xử lý tìm kiếm/cào dữ liệu dựa trên từ khóa
    ket_qua_tim_kiem = cao_du_lieu_so_sanh(keyword)
    
    # Trả về trang index.html cùng với từ khóa và danh sách kết quả tìm được
    return render_template('index.html', keyword=keyword, results=ket_qua_tim_kiem)


if __name__ == '__main__':
    # Chạy ứng dụng dưới Local (máy tính của bro)
    app.run(debug=True)