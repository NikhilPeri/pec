import sys
import time
from src.pec.cache import PriorityExpiryCache

def test_set_evicts_based_on_expiry():
    cache = PriorityExpiryCache(3)

    cache.set('A', 'value', priority=1, expiry=sys.maxsize)
    cache.set('B', 'value', priority=1, expiry=1)
    cache.set('C', 'value', priority=1, expiry=sys.maxsize)
    cache.set('D', 'value', priority=1, expiry=sys.maxsize)

    assert set(cache.keys()) == {'A', 'C', 'D'}

def test_set_evicts_based_on_priority():
    cache = PriorityExpiryCache(3)

    cache.set('A', 'value', priority=1, expiry=sys.maxsize)
    time.sleep(1e-3)
    cache.set('B', 'value', priority=2, expiry=sys.maxsize)
    time.sleep(1e-3)
    cache.set('C', 'value', priority=3, expiry=sys.maxsize)
    time.sleep(1e-3)
    cache.set('D', 'value', priority=1, expiry=sys.maxsize)

    assert set(cache.keys()) == {'A', 'B', 'D'}

def test_set_evicts_based_on_access_time():
    cache = PriorityExpiryCache(3)

    cache.set('A', 'value', priority=1, expiry=sys.maxsize)
    cache.set('B', 'value', priority=1, expiry=sys.maxsize)
    cache.set('C', 'value', priority=1, expiry=sys.maxsize)

    cache.get('A')
    cache.set('D', 'value', priority=1, expiry=sys.maxsize)

    assert set(cache.keys()) == {'A', 'C', 'D'}


def test_set_updates_existing_values():
    cache = PriorityExpiryCache(3)

    cache.set('A', 'old_value', priority=1)
    cache.set('A', 'new_value', priority=2)

    item = cache.get_item('A')
    assert item.value == 'new_value'
    assert item.priority == 2
