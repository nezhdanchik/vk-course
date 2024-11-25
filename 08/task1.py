import weakref
from time import perf_counter

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class PointSlots:
    __slots__ = ['x', 'y', '__weakref__']
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class PointWithWeakRef:
    def __init__(self, x, y):
        self.ref_x = weakref.ref(x)
        self.ref_y = weakref.ref(y)

    @property
    def x(self):
        return self.ref_x().value

    @x.setter
    def x(self, value):
        self.ref_x().value = value

    @property
    def y(self):
        return self.ref_y().value

    @y.setter
    def y(self, value):
        self.ref_y().value = value

def timer(func):
    def inner(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        print(f'Для {func.__name__} сработало за {perf_counter() - start:.6f}')
        return result
    return inner

@timer
def create_bunch(n, cls, *args):
    res = [cls(*args) for _ in range(n)]
    print(f'Создано {n} объектов {cls.__name__}{args}')
    return res

@timer
def read_update_bunch(bunch):
    for obj in bunch:
        a = obj.x
        b = obj.y
        obj.x += 1
        obj.y += 1

class IntWrapper:
    __slots__ = ('value', '__weakref__')
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, int):
            return IntWrapper(self.value + other)
        return IntWrapper(self.value + other.value)

    def __repr__(self):
        return str(self.value)

def test_point_class_speed(cls, count_points= 10**6):
    print(f'------------Тестирование {cls.__name__=}--------------------')
    one = IntWrapper(1)
    points = create_bunch(count_points, cls, one, one)
    read_update_bunch(points)
    print('-------------------------------------------------------------')

if __name__ == '__main__':
    for point_cls in Point, PointSlots, PointWithWeakRef:
        test_point_class_speed(point_cls)