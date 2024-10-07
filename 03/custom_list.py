class CustomList(list):

    def __str__(self):
        return f'{super().__str__()} Sum: {sum(self)}'

    def __add__(self, other):
        if isinstance(other, int):
            return CustomList([self[i] + other for i in range(len(self))])
        if isinstance(other, list):
            min_length = min(len(self), len(other))
            result = CustomList()
            for i in range(min_length):
                result.append(self[i] + other[i])
            if len(self) > len(other):
                result.extend(self[min_length:])
            elif len(self) < len(other):
                result.extend(other[min_length:])
            return result
        raise NotImplementedError(f'Тип {type(other)} не поддерживается')

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, int):
            return CustomList([i - other for i in self])
        return self.__add__([-i for i in other])

    def __rsub__(self, other):
        return CustomList([-i for i in self.__sub__(other)])

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __eq__(self, other):
        return sum(self) == sum(other)

    # для тестов
    def eq_elements(self, other):
        return list(self) == list(other)
