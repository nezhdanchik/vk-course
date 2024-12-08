from descriptor import PnoneNumberRussia, Name, PositiveInteger
import pytest


def test_name_no_params():
    class Person:  # pylint: disable=too-few-public-methods
        name = Name()

        def __init__(self, name):
            self.name = name

    p = Person('Petya')
    assert p.name == 'Petya'
    p = Person('X')
    assert p.name == 'X'
    p = Person('X' * 100)
    assert p.name == 'X' * 100

    with pytest.raises(TypeError):
        p = Person(123)

    with pytest.raises(ValueError):
        p = Person('')

    with pytest.raises(ValueError):
        p = Person('!')

    with pytest.raises(ValueError):
        p = Person('Vasy1')


def test_name_max_length():
    class Person:  # pylint: disable=too-few-public-methods
        name = Name(max_length=15)

        def __init__(self, name):
            self.name = name

    p = Person('Petya')
    assert p.name == 'Petya'
    with pytest.raises(ValueError):
        p = Person('X' * 100)

    p = Person('X' * 15)
    with pytest.raises(ValueError):
        p = Person('X' * 16)


def test_positive_integer_strong():
    class Person:  # pylint: disable=too-few-public-methods
        age = PositiveInteger(strong=True)

        def __init__(self, age):
            self.age = age

    p = Person(10)
    assert p.age == 10

    with pytest.raises(ValueError):
        p = Person(-1)

    with pytest.raises(TypeError):
        p = Person('10')


def test_positive_integer_not_strong():
    class Person:  # pylint: disable=too-few-public-methods
        age = PositiveInteger(strong=False)

        def __init__(self, age):
            self.age = age

    p = Person(-5)
    assert p.age == 0

    p = Person(0)
    assert p.age == 0


def test_phone():
    class Person:  # pylint: disable=too-few-public-methods
        phone = PnoneNumberRussia()

        def __init__(self, phone):
            self.phone = phone

    with pytest.raises(ValueError):
        p = Person('')

    p = Person('+7(123)456-78-90')
    assert p.phone == '+7(123)456-78-90'

    with pytest.raises(ValueError):
        p = Person('+7-123-456-78-90')

    with pytest.raises(ValueError):
        p = Person('+7(123)4567890')

    with pytest.raises(ValueError):
        p = Person('8(123)456-78-90')


def test_many_fields():
    class Person:  # pylint: disable=too-few-public-methods
        own_age = PositiveInteger(strong=True)
        child_age = PositiveInteger(strong=False)

        def __init__(self, own_age, child_age):
            self.own_age = own_age
            self.child_age = child_age

    p = Person(40, 10)
    assert p.own_age == 40
    assert p.child_age == 10


def test_change_from_valid_to_invalid():
    class Person:  # pylint: disable=too-few-public-methods
        age = PositiveInteger(strong=False)
        number = PnoneNumberRussia()
        name = Name(max_length=10)

        def __init__(self, age, number, name):
            self.age = age
            self.number = number
            self.name = name

    p = Person(10, '+7(123)456-78-90', 'danya')
    assert p.age == 10
    p.age = -10
    assert p.age == 0
    assert p.number == '+7(123)456-78-90'
    with pytest.raises(ValueError):
        p.number = '+7-123-456-78-90'
    assert p.number == '+7(123)456-78-90'

    with pytest.raises(ValueError):
        p.name = ''
    with pytest.raises(ValueError):
        p.name = '!'
    with pytest.raises(ValueError):
        p.name = 'd' * 11

    assert p.name == 'danya'
