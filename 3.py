import math

class Point:
    def __init__(self, x=0, y=1):
        self.__x = x
        self.__y = y

    def read(self):
        try:
            parts = input().split()
            if len(parts) >= 2:
                self.__x = int(parts[0])
                self.__y = int(parts[1])
        except EOFError:
            pass

    def print(self):
        print(f"({self.__x}, {self.__y})", end="")

    def move(self, dx, dy):
        self.__x += dx
        self.__y += dy

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def setXY(self, x, y):
        self.__x = x
        self.__y = y

    def distance(self, other=None):
        if other is None:
            return math.sqrt(self.__x**2 + self.__y**2)
        return math.sqrt((self.__x - other.getX())**2 + (self.__y - other.getY())**2)

    def __str__(self):
        return f"({self.__x}, {self.__y})"


class ColorPoint(Point):
    def __init__(self, *args):
        # Hàm xây dựng không đối số
        if len(args) == 0:
            super().__init__(0, 1)
            self.color = "xanh"
        # Hàm xây dựng sao chép (1 đối số là ColorPoint)
        elif len(args) == 1:
            super().__init__(args[0].getX(), args[0].getY())
            self.color = args[0].color
        # Hàm xây dựng 3 đối số (x, y, color)
        elif len(args) == 3:
            super().__init__(args[0], args[1])
            self.color = args[2]

    def read(self):
        try:
            parts = input().split()
            if len(parts) >= 3:
                self.setXY(int(parts[0]), int(parts[1]))
                self.color = parts[2]
        except EOFError:
            pass

    def print(self):
        super().print()
        print(f": {self.color}")

    def setColor(self, color):
        self.color = color

    def __str__(self):
        return f"{super().__str__()}: {self.color}"