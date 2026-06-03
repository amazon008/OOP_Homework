import math

class Point:
    def __init__(self, x=0, y=1):
        self.__x = x
        self.__y = y

    def read(self):
        self.__x, self.__y = map(int, input().split())

    def print(self):
        print(f"({self.__x}, {self.__y})")

    def move(self, dx, dy):
        self.__x += dx
        self.__y += dy

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def distance(self, p=None):
        if p is None:
            return math.sqrt(self.__x**2 + self.__y**2)
        return math.sqrt((self.__x - p.getX())**2 + (self.__y - p.getY())**2)

    def __str__(self):
        return f"({self.__x}, {self.__y})"


class LineSegment:
    def __init__(self, *args):
        if len(args) == 0:
            self.__d1 = Point(8, 5)
            self.__d2 = Point(1, 0)
        elif len(args) == 1:
            # Sao chép sâu đối tượng LineSegment S
            other = args[0]
            self.__d1 = Point(other._LineSegment__d1.getX(), other._LineSegment__d1.getY())
            self.__d2 = Point(other._LineSegment__d2.getX(), other._LineSegment__d2.getY())
        elif len(args) == 2:
            # Lấy d1 và d2 làm hai điểm đầu mút, không tạo thêm điểm mới (sao chép nông/tham chiếu)
            self.__d1 = args[0]
            self.__d2 = args[1]
        elif len(args) == 4:
            self.__d1 = Point(args[0], args[1])
            self.__d2 = Point(args[2], args[3])

    def read(self):
        coords = list(map(int, input().split()))
        self.__d1 = Point(coords[0], coords[1])
        self.__d2 = Point(coords[2], coords[3])

    def print(self):
        print(self)

    def __str__(self):
        return f"[{self.__d1}; {self.__d2}]"

    def move(self, dx, dy):
        self.__d1.move(dx, dy)
        self.__d2.move(dx, dy)

    def length(self):
        return self.__d1.distance(self.__d2)

    def angle(self):
        dx = self.__d2.getX() - self.__d1.getX()
        dy = self.__d2.getY() - self.__d1.getY()
        ang = round(math.degrees(math.atan2(dy, dx)))
        return (ang % 360 + 360) % 360


class LineSegmentTest:
    def testCase(self):
        # Đọc 4 số nguyên từ stdin và tạo ls1
        coords = list(map(int, input().split()))
        ls1 = LineSegment(coords[0], coords[1], coords[2], coords[3])
        
        # In thông tin ls1, chiều dài và góc
        ls1.print()
        print(ls1.length())
        print(ls1.angle())
        
        # Tạo ls2 là bản sao chép sâu của ls1
        ls2 = LineSegment(ls1)
        
        # Tịnh tiến ls1 đi 1 độ dời (1, 1)
        ls1.move(1, 1)
        
        # In ls1 (đã dời) và ls2 (giữ nguyên do sao chép sâu)
        ls1.print()
        ls2.print()