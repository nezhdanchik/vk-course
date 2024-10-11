class Base:
    def __set_name__(self, owner, name):
        self._name = f'_hidden_{name}' # pylint: disable=W0201

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self._name)

    def __delete__(self, instance):
        delattr(instance, self._name)

    def __set__(self, instance, value):
        raise NotImplementedError(
            'This method should be implemented in subclass')

    @staticmethod
    def check_type_with_exception(value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(f'not {expected_type} type')


class PnoneNumberRussia(Base):
    '''Номер вида +7(999)999-99-99'''

    def __set__(self, instance, value):
        self.check_type_with_exception(value, str)
        if len(value) != 16:
            raise ValueError('not valid structure of phone number')
        conditions = [
            value[0] == '+',
            value[1] == '7',
            value[2] == '(',
            value[6] == ')',
            value[10] == '-',
            value[13] == '-',
        ]
        if not all(conditions):
            raise ValueError('not valid structure of phone number')
        for ind, val in enumerate(value):
            if ind in [0, 1, 2, 6, 10, 13]:
                continue
            if not val.isdigit():
                raise ValueError('not digit')
        setattr(instance, self._name, value)


class Name(Base):
    '''Не пустая строка'''

    def __init__(self, max_length=None):
        self.max_length = max_length

    def __set__(self, instance, value):
        self.check_type_with_exception(value, str)
        if len(value) == 0:
            raise ValueError('empty string')
        if self.max_length and len(value) > self.max_length:
            raise ValueError('too long string')
        for char in value:
            if not char.isalpha():
                raise ValueError('not alpha')
        setattr(instance, self._name, value)


class PositiveInteger(Base):

    def __init__(self, strong=True):
        self.strong = strong

    def __set__(self, instance, value):
        self.check_type_with_exception(value, int)
        if self.strong and value < 0:
            raise ValueError('not positive')
        value = max(0, value)
        setattr(instance, self._name, value)
