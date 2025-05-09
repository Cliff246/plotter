


class ValidatorObj:
	"""
	contains validation states
	"""


	def __init__(self, key_type: object, key: any, valid_values_types: object | list[object], must_be: list[list[any] | None] = None, flags: list[str]= [""]):

		if not isinstance(key_type, object):
			raise TypeError("key type is not valid")
		if isinstance(key_type, key):
			raise TypeError("key type must be the same type as key")
		length: int = -1
		if not isinstance(valid_values_types, list) or not isinstance(valid_values_types, object):
			if isinstance(valid_values_types, list):
				for T in valid_values_types:
					if not isinstance(T, object):
						raise TypeError("element in valid values_types must be object")
				length = len(valid_values_types)
				if must_be != None:
					if not isinstance(must_be, list):
						TypeError("must be has to be of type list[tuple[int, list[any] | None]]")
					if len(must_be) != length:
						



		self.key_type =  key_type
		self.key = key
		self.valid_values_types = valid_values_types
		self.must_be: list[tuple[int, list[any]]] = must_be
		self.flags: list[str] = [""]
