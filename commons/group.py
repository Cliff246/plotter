


class Group:

	def __init__(self, key: str, meta: dict, contents: list):

		self.key: str = key
		self.meta: dict  = meta
		self.contents: list = contents



	def __getitem__(self, key):
		if(isinstance(key, int)):
			return self.contents[key]

	def __len__(self):
		return len(self.contents)

	def __iter__(self):
		return iter(self.contents)



