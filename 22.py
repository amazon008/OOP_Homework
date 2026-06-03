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
            self.__d1 = Point(args[0].__d1.getX(), args[0].__d1.getY())
            self.__d2 = Point(args[0].__d2.getX(), args[0].__d2.getY())
        elif len(args) == 2:
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