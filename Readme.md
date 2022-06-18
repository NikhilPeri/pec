# PEC

## Installation

```
pip install
```

## Usage
The following example will create a PriorityExpiryCache of maxsize 3. It will cache up to 3 items and evict items based
on the following strategy:
 - Evict ONE expired entry first
 - If there are no expired items to evict then evict the lowest priority entries
 - Tie breaking among entries with the same priority is done via least recently used.

```python
from pec import PriorityExpiryCache

cache = PriorityExpiryCache(3)

cache.set('A', 'value', priority=1, expiry=sys.maxsize)
cache.set('B', 'value', priority=1, expiry=1)
cache.set('C', 'value', priority=1, expiry=sys.maxsize)
cache.set('D', 'value', priority=1, expiry=sys.maxsize)

assert set(cache.keys()) == {'A', 'C', 'D'}
```

## Testing
This code base has unit tests.  After cloning you can run `pytest` to run the test cases located in "/test/test_cache.py"


## Implementation
This PEC cache is implemented by indexing items by three fields
  - priority
  - expiry
  - access time

The indexes are implemented use [blist]() which is an open source python implementation of sorted dictionaries and lists
using a binary search tree as the undelying datastructure

The image below shows how the indexs are structured to quickly query items based on oldest expiration, lowest priorty, least accessed
