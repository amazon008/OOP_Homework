import math

class Point:
    # Kết hợp cả 2 hàm xây dựng bằng tham số mặc định
    def __init__(self, x=None, y=None):
        if x is None and y is None:
            self.__x = 0 
            self.__y = 1
        else:
            self.__x = x
            self.__y = y

    # Nhập tọa độ cho điểm từ bàn phím
    def read(self):
        # Đọc 1 dòng, tách theo khoảng trắng và chuyển sang kiểu int
        parts = input().split()
        if len(parts) >= 2:
            self.__x = int(parts[0])
            self.__y = int(parts[1])

    # Hiển thị dữ liệu ra màn hình
    def print(self):
        # Hàm print trong Python mặc định đã có xuống dòng ở cuối
        print(f"({self.__x}, {self.__y})")

    # Dời điểm đi 1 độ dời (dx, dy)
    def move(self, dx, dy):
        self.__x += dx
        self.__y += dy

    # Lấy ra giá trị hoành độ
    def getX(self):
        return self.__x

    # Lấy ra giá trị tung độ
    def getY(self):
        return self.__y

    # Kết hợp 2 hàm tính khoảng cách bằng tham số P mặc định là None
    def distance(self, P=None):
        if P is None:
            # Khoảng cách đến gốc tọa độ
            return math.sqrt(self.__x**2 + self.__y**2)
        else:
            # Khoảng cách đến điểm P
            return math.sqrt((P.getX() - self.__x)**2 + (P.getY() - self.__y)**2)
        # ==========================================
# Phần code dưới đây dùng để chạy thử chương trình
# (Tương đương với hàm main() trong C++)
# ==========================================

if __name__ == "__main__":
    print("--- Chuong trinh test lop Point ---")
    
    # Tạo điểm mặc định
    p1 = Point()
    print("Diem p1 (mac dinh):", end=" ")
    p1.print()

    # Nhập điểm từ bàn phím
    p2 = Point()
    print("Nhap toa do x y cho diem p2 (cach nhau boi dau cach):")
    p2.read()
    
    print("Diem p2 ban vua nhap la:", end=" ")
    p2.print()

    print(f"Khoang cach tu p2 den goc toa do la: {p2.distance()}")