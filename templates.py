import os
import hashlib
#to change later
TEMPLATES_SOURCE_DIR = "templates"

def compare_str_hashes(a, b):
	if(isinstance(a, str) and isinstance(b, str)):
		if(len(a) == len(b)):
			if(a == b):
				return True
			return False
		raise ValueError("length of a and b strings is not the same")
	raise TypeError("both a and b must be strings")

class Template:

	def __init__(self, key, value):


		self.key = key
		self.value = value

		self.my_path: str = None
		self.set_path()

	def look_through_templates_dir(self):
		if self.my_path is None:
			return None

		templates = os.listdir(TEMPLATES_SOURCE_DIR)
		template_base = self.value.get("template_path", "")
		hash_value = self.value.get("hash", "")

		preferred = f"{template_base}_{hash_value[:8]}.py" if hash_value else f"{template_base}.py"

		if preferred in templates:
			return os.path.join(TEMPLATES_SOURCE_DIR, preferred)

		# Fallback candidates
		candidates = [f for f in templates if f.startswith(template_base) and f.endswith(".py")]

		if not candidates:
			return None

		if not hash_value:
			# Prefer un-hashed version first
			for f in candidates:
				if "_" not in f.rstrip(".py"):
					return os.path.join(TEMPLATES_SOURCE_DIR, f)
			return os.path.join(TEMPLATES_SOURCE_DIR, candidates[0])

		# If we had a hash, fallback to partial match
		for f in candidates:
			if hash_value[:8] in f:
				return os.path.join(TEMPLATES_SOURCE_DIR, f)

		return os.path.join(TEMPLATES_SOURCE_DIR, candidates[0])

	def set_path(self):
		if not isinstance(self.value, dict):
			raise TypeError("Template 'value' must be a dictionary.")

		template_path = self.value.get("template_path")
		if not isinstance(template_path, str) or not template_path:
			raise ValueError("Template must have a non-empty 'template_path' string.")

		hash_value = self.value.get("hash")
		if hash_value is not None and not isinstance(hash_value, str):
			raise ValueError("'hash' must be a string if provided.")

		if hash_value:
			self.set_hashed_path()
		else:
			self.set_normal_path()

	def set_normal_path(self):

		self.my_path = "%s.py" % self.value["template_path"]


	def set_hashed_path(self):

		self.my_path = "%s_%.8s.py" % (self.value["template_path"], self.value["hash"])

	def __getitem__(self, item):
		return self.value[item]

	def __contains__(self, item):
		return item in self.value