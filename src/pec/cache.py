import sys
import time

from blist import sorteddict, sortedlist
from collections import deque


class Item:
	def __init__(self, key, value, priority, expiry, access_time):
		self.key = key
		self.value = value
		self.priority = priority
		self.expiry = expiry
		self.access_time = access_time

	def __iter__(self):
		return self.key, self.value, self.priority, self.expiry, self.access_time

class PriorityExpiryCache:
	def __init__(self, max_items):
		self.max_items = max_items
		self.key_index = {}
		self.priority_index = sorteddict({})
		self.expiry_index = sortedlist([], key=lambda x: x[0])

	def set(self, key, value, priority=1, expiry=sys.maxsize):
		if len(self) >= self.max_items:
			self._evict_items()

		if key in self.key_index:
			existing_item = self.key_index[key]
			self._delete_item(existing_item)
			self.set(key, value, priority=priority, expiry=expiry)
			return

		item = Item(key, value, priority, expiry, time.time_ns())
		self.key_index[key] = item

		if item.priority not in self.priority_index:
			self.priority_index[item.priority] = sortedlist([], key=lambda x: x[0])
		self.priority_index[item.priority].add((item.access_time, item))
		self.expiry_index.add((item.expiry, item))

	def get(self, key):
		item = self.get_item(key)
		return item.value

	def get_item(self, key):
		self._update_access_time(key)
		return self.key_index[key]

	def _evict_items(self):
		while len(self.key_index) >= self.max_items:
			self._evict_item()

	def _evict_item(self):
			# Evict expired item
			earliest_expiry, item = self.expiry_index[0]
			if earliest_expiry < time.time_ns():
				self._delete_item(item)
				return

			# Evict least accessed lowest priorty
			lowest_priorty = max(self.priority_index._map.keys()) # TODO: the blist.sorteddict.keys function this was a hack
			_, item = self.priority_index[lowest_priorty][0]
			self._delete_item(item)

	def _delete_item(self, item):
		# Remove from priority index
		self.priority_index[item.priority].remove((item.access_time, item))
		if len(self.priority_index[item.priority]) == 0:
			del self.priority_index[item.priority]

		# Remove from expiry index
		self.expiry_index.remove((item.expiry, item))

		# Remove from key index
		del self.key_index[item.key]

	def _update_access_time(self, key):
		access_time = time.time_ns()
		item = self.key_index[key]

		self.priority_index[item.priority].remove((item.access_time, item))
		item.access_time = access_time
		self.priority_index[item.priority].add((item.access_time, item))


	def keys(self):
		return self.key_index.keys()

	def __len__(self):
		return len(self.key_index)
