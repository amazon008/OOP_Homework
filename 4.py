class TuLanh:
    def __init__(self, nhanhieu="Elextrolux", maso="UNKNOWN", nuocsx="Việt Nam", tkdien=True, dungtich=256, gia=7000000):
        self.__nhanhieu = nhanhieu
        self.__maso = maso
        self.__nuocsx = nuocsx
        self.__tkdien = tkdien
        self.__dungtich = dungtich
        self.__gia = gia

    def makeCopy(self, tl):
        self.__nhanhieu = tl.__nhanhieu
        self.__maso = tl.__maso
        self.__nuocsx = tl.__nuocsx
        self.__tkdien = tl.__tkdien
        self.__dungtich = tl.__dungtich
        self.__gia = tl.__gia

    def nhapThongTin(self):
        try:
            self.__nhanhieu = input().strip()
            self.__maso = input().strip()
            self.__nuocsx = input().strip()
            tk = input().strip().lower()
            self.__tkdien = True if (tk == 'true' or tk == '1') else False
            self.__dungtich = int(input().strip())
            self.__gia = int(input().strip())
        except EOFError:
            pass

    def hienThi(self):
        print("============")
        # KHÔNG có dấu cách trước dấu hai chấm, và CÓ đúng 1 dấu cách sau dấu hai chấm
        print(f"Nhãn hiệu: {self.__nhanhieu}")
        print(f"Mã số: {self.__maso}")
        print(f"Nước SX: {self.__nuocsx}")
        
        tk_str = "Có" if self.__tkdien else "Không"
        print(f"T/K điện: {tk_str}")
        
        print(f"Dung tích: {self.__dungtich}L")
        print(f"Giá: {self.__gia}")
        print("============")

    def layNhanHieu(self):
        return self.__nhanhieu

    def layGia(self):
        return self.__gia

    def soNguoiSD(self):
        return self.__dungtich // 100

    def cungNhanHieu(self, tl):
        return self.__nhanhieu == tl.__nhanhieu

    def nhoHon(self, tl):
        return self.__dungtich < tl.__dungtich


class TuLanhTest:
    # Sử dụng @staticmethod phòng trường hợp hệ thống gọi thẳng TuLanhTest.testCase() mà không tạo đối tượng
    @staticmethod
    def testCase():
        # 1. Tạo đối tượng t1, rồi xuất thông tin của t1
        t1 = TuLanh()
        t1.hienThi()

        # 2. Tạo đối tượng t2, nhập dữ liệu từ bàn phím, rồi xuất t2
        t2 = TuLanh()
        t2.nhapThongTin()
        t2.hienThi()

        # 3. Tạo đối tượng t3, chép dữ liệu từ t2 sang t3
        t3 = TuLanh()
        t3.makeCopy(t2)

        # 4. Kiểm tra t2, t1 có cùng nhãn hiệu không
        if t2.cungNhanHieu(t1):
            print("t2, t1 cung nhan hieu")
        else:
            print("t2, t1 khong cung nhan hieu")

        # 5. Kiểm tra t2 có nhỏ hơn t1 không
        if t2.nhoHon(t1):
            print("t2 nho hon t1")
        else:
            print("t2 khong nho hon t1")