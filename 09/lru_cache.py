import logging
import argparse
from collections import abc

# parsing args
parser = argparse.ArgumentParser(description="LRU cache")

parser.add_argument(
    "-s", action="store_true", help="Дополнительное логирование в stdout"
)
parser.add_argument("-f", action="store_true", help="кастомный фильтр")

args = vars(parser.parse_args())


# pylint: disable=R0903
class Filter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.INFO


logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler_file = logging.FileHandler(f"{__name__}.log", mode="w")
handler_file.setFormatter(formatter)
handler_stream = logging.StreamHandler()
handler_stream.setFormatter(formatter)

logger.addHandler(handler_file)
logger.setLevel(logging.DEBUG)

if args["s"]:
    logger.addHandler(handler_stream)

if args["f"]:
    handler_stream.addFilter(Filter())


class EmptyException(BaseException):
    pass


class MyDict(dict):
    def move_elem_to_end(self, key):
        logger.debug("Move elem to end: %s", key)
        val = self[key]
        del self[key]
        self[key] = val

    def remove_first_elem(self):
        logger.debug("Removing first elem")
        if len(self) > 0:
            del self[next(iter(self))]
        else:
            logger.error("Trying to remove first elem from empty dict")
            raise EmptyException("dict is empty, can't remove first elem")


# LRU - Last Recently Used
class LRUCache:
    def __init__(self, limit=42):
        logger.info("Creating instance with limit %d", limit)
        if limit <= 0:
            logger.error(
                "It's prohibited to create cache with limit %d <= 0", limit
            )
            raise ValueError("Limit must be > 0")
        self.limit = limit
        self._data = MyDict()

    def get_data_keys(self):
        logger.info("Getting all keys")
        return tuple(self._data.keys())

    def get(self, key):
        logger.info("Getting value for key %s", key)
        if key not in self._data:
            logger.warning("Key %s not found", key)
            return None
        self._data.move_elem_to_end(key)
        return self._data[key]

    def set(self, key, value):
        logger.info("Setting value %s for key %s", value, key)
        if not isinstance(key, abc.Hashable):
            logger.error("Trying to set key %s which is not hashable", key)
            raise TypeError("Key must be hashable")
        if len(self._data) == self.limit:
            logger.info("Limit reached, removing first elem")
            self._data.remove_first_elem()
        self._data[key] = value

    def __getitem__(self, item):
        logger.debug("Getting value via [%s]", item)
        return self.get(item)

    def __setitem__(self, key, value):
        logger.debug("Setting value via [%s] = %s", key, value)
        self.set(key, value)


if __name__ == "__main__":
    lru = LRUCache(4)
    lru.set("a", 1)
    lru.set("b", 2)
    lru.set("c", 3)

    lru.get("a")
    lru.get("d")
    lru.set("d", 4)
    lru.set("e", 5)
    lru.set("e", 55)
