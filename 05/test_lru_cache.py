from random import random
from time import perf_counter
import numpy as np
import pytest

from lru_cache import LRUCache


def test_before_limit():
    cache = LRUCache(2)
    cache.set("k1", "val1")
    cache["k2"] = "val2"
    assert cache.get('k1') == 'val1'
    assert cache['k2'] == 'val2'


def test_exceed_limit():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    _, _ = cache['k2'], cache['k1']

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"


def test_get():
    cache = LRUCache(3)
    assert cache.get("k1") is None
    cache.set("k1", "val1")
    assert cache.get("k1") == "val1"
    cache["k2"] = "val2"
    assert cache["k2"] == "val2"


def test_set():
    cache = LRUCache(3)
    cache["k1"] = "val1"
    cache['k1'] = 'val2'
    assert cache['k1'] == 'val2'

    with pytest.raises(TypeError):
        cache[{1: 2}] = 'val3'


def test_bad_limit():
    with pytest.raises(ValueError):
        LRUCache(0)
    with pytest.raises(ValueError):
        LRUCache(-10)


def test_not_existing_key():
    cache = LRUCache()
    assert cache[1] is None


def stress_time(quantity, limit=100):
    start = perf_counter()
    cache = LRUCache(limit=limit)
    # set
    for _ in range(quantity):
        cache.set(random(), random())

    # get
    for key in cache.get_data_keys():
        cache.get(key)

    end = perf_counter()
    return end - start


def test_stress_time():
    '''
    Если операции set и get выполняются за приблизительно
    O(1), то выполнение n раз подряд этих операций должно занимать
    примерно O(n).
    '''
    quantities = list(np.linspace(10 ** 3, 10 ** 6, 20, dtype=int))
    times = [stress_time(quantity) for quantity in quantities]
    print()
    rates = []
    # pylint: disable=C0200
    for i in range(len(quantities)):
        rates.append(quantities[i] / times[i])

    # стандартное отклонение отклоняется не более чем на 15% от среднего
    mean_rate = np.mean(rates)
    std_rate = np.std(rates)
    threshold = 0.15 * mean_rate
    print(f'{mean_rate=}, {std_rate=}, {threshold=}')
    assert std_rate < threshold
