import weakref
from time import perf_counter
from abc import ABC


class Person(ABC):
    def __init__(self, age):
        self.age = age

    def __repr__(self):
        return f'{self.age}'


class PersonDictAttrs(Person):
    ...


class PersonSlots(Person):
    __slots__ = ('age',)


class PersonWithWeakRef(Person):
    def __init__(self, age):
        self.ref_age = weakref.ref(age)

    @property
    def age(self):
        return self.ref_age()


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
        _ = obj.age
        obj.age.change(5)


class IntWrapper:
    __slots__ = ('value', '__weakref__')

    def __init__(self, value):
        self.value = value

    def change(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


def test_class_speed(cls, count=10 ** 6):
    print(f'Тестирование {cls.__name__=}'.center(80, '-'))
    one = IntWrapper(1)
    persons = create_bunch(count, cls, one)
    read_update_bunch(persons)
    print('-' * 80)


if __name__ == '__main__':
    for cls in PersonDictAttrs, PersonSlots, PersonWithWeakRef:
        test_class_speed(cls, count=10**6*5)
