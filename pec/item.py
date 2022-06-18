class Item:
	def __init__(self, key, value, priority, expiry, access_time):
		self.key = key
		self.value = value
		self.priority = priority
		self.expiry = expiry
		self.access_time = access_time

	def __iter__(self):
		return self.key, self.value, self.priority, self.expiry, self.access_time
