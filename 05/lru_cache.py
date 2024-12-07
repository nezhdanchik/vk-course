from collections import abc


class EmptyException(BaseException):
    pass


class MyDict(dict):
    def move_elem_to_end(self, key):
        val = self[key]
        del self[key]
        self[key] = val

    def remove_first_elem(self):
        if len(self) > 0:
            del self[next(iter(self))]
        else:
            raise EmptyException('dict is empty, can\'t remove first elem')


# LRU - Last Recently Used
class LRUCache:
    def __init__(self, limit=42):
        if limit <= 0:
            raise ValueError('Limit must be > 0')
        self.limit = limit
        self._data = MyDict()

    def get_data_keys(self):
        return tuple(self._data.keys())

    def get(self, key):
        if key not in self._data:
            return None
        self._data.move_elem_to_end(key)
        return self._data[key]

    def set(self, key, value):
        if not isinstance(key, abc.Hashable):
            raise TypeError('Key must be hashable')
        if len(self._data) == self.limit:
            self._data.remove_first_elem()
        self._data[key] = value
        self._data.move_elem_to_end(key)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)
