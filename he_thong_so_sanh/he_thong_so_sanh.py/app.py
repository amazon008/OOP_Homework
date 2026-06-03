from flask import Flask, render_template, request

app = Flask(__name__)

# 1. DỮ LIỆU GIẢ LẬP (Ngày 3 mình sẽ cấu hình để đọc dữ liệu thật từ SQLite vào đây)
DATA = [
    {"san_pham": "iPhone 15 Pro Max - 256GB", "cua_hang": "Hoàng Hà Mobile", "gia": 29000000, "danh_gia": "⭐ 4.5", "link": "https://hoanghamobile.com"},
    {"san_pham": "iPhone 15 Pro Max - 256GB", "cua_hang": "CellphoneS", "gia": 29500000, "danh_gia": "⭐ 4.8", "link": "https://cellphones.com.vn"},
    {"san_pham": "Samsung Galaxy S24 Ultra - 256GB", "cua_hang": "Hoàng Hà Mobile", "gia": 25000000, "danh_gia": "⭐ 4.7", "link": "https://hoanghamobile.com"},
    {"san_pham": "Samsung Galaxy S24 Ultra - 256GB", "cua_hang": "Di Động Việt", "gia": 24800000, "danh_gia": "⭐ 4.9", "link": "https://didongviet.vn"}
]

@app.route('/')
def index():
    # Lấy từ khóa người dùng gõ từ thanh tìm kiếm (Ví dụ: /?q=iPhone)
    query = request.args.get('q', '').strip()
    ket_qua = {}

    if query:
        # Lọc các sản phẩm có tên chứa từ khóa tìm kiếm (không phân biệt hoa thường)
        filtered_data = [item for item in DATA if query.lower() in item['san_pham'].lower()]

        # Nhóm các cửa hàng bán cùng một loại máy lại với nhau
        for item in filtered_data:
            sp = item['san_pham']
            if sp not in ket_qua:
                ket_qua[sp] = []
            ket_qua[sp].append(item)

        # LOGIC TÌM GIÁ RẺ NHẤT: Duyệt qua từng nhóm sản phẩm để cắm cờ "la_re_nhat"
        for sp, cua_hangs in ket_qua.items():
            gia_min = min(item['gia'] for item in cua_hangs)
            for item in cua_hangs:
                # Nếu giá cửa hàng này bằng giá thấp nhất trong nhóm thì đánh dấu True
                item['la_re_nhat'] = (item['gia'] == gia_min)
                # Định dạng lại số tiền thành chuỗi có dấu phẩy cho dễ đọc (VD: 29,000,000 đ)
                item['gia_hien_thi'] = f"{item['gia']:,} ₫"

    # Gửi dữ liệu sang file giao diện index.html để hiển thị
    return render_template('index.html', ket_qua=ket_qua, query=query)

if __name__ == '__main__':
    # Bật debug=True để khi bro sửa code, web sẽ tự động cập nhật không cần bật lại
    app.run(debug=True)