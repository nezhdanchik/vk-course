import logging
from collections import abc

logger = logging.getLogger(__name__)
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)



class EmptyException(BaseException):
    pass


class MyDict(dict):
    def move_elem_to_end(self, key):
        logger.debug(f'Перемещение элемента с ключом {key} в конец')
        val = self[key]
        del self[key]
        self[key] = val

    def remove_first_elem(self):
        logger.debug('Удаление первого элемента')
        if len(self) > 0:
            del self[next(iter(self))]
        else:
            logger.error('Попытка удалить первый элемент из пустого словаря')
            raise EmptyException('dict is empty, can\'t remove first elem')


# LRU - Last Recently Used
class LRUCache:
    def __init__(self, limit=42):
        logger.info(f'Создание экземпляра с лимитом {limit}')
        if limit <= 0:
            logger.error(f'Запрещено создавать кэш с лимитом {limit} <= 0')
            raise ValueError('Limit must be > 0')
        self.limit = limit
        self._data = MyDict()

    def get_data_keys(self):
        logger.info('Получение всех ключей')
        return tuple(self._data.keys())

    def get(self, key):
        logger.info(f'Получение значения для ключа {key}')
        if key not in self._data:
            return None
        self._data.move_elem_to_end(key)
        return self._data[key]

    def set(self, key, value):
        logger.info(f'Установка значения {value} для ключа {key}')
        if not isinstance(key, abc.Hashable):
            logger.error(f'Попытка установить ключ {key}, который не является хешируемым')
            raise TypeError('Key must be hashable')
        if len(self._data) == self.limit:
            logger.info('Достигнут лимит, удаляем первый элемент')
            self._data.remove_first_elem()
        self._data[key] = value

    def __getitem__(self, item):
        logger.debug(f'Получение значения с помощью [{item}]')
        return self.get(item)

    def __setitem__(self, key, value):
        logger.debug(f'Установка значения с помощью [{key}] = {value}')
        self.set(key, value)

l = LRUCache(1)
l.set('k1', 'v1')
l.set('k2', 'v2')