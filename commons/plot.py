import json



class Plot:

	def __init__(self, manifest_info: dict):
		assert(isinstance(manifest_info, dict) and "manifest info must be a dict")
		self.manifest_info: dict = manifest_info
		self.meta: dict = dict()
		self.data: dict = dict()
		if("source" not in self.manifest_info):
			raise ValueError("source must be in manifest info")
		self.path = self.manifest_info["source"]
		self.loaded = False

	def read_data(self):
		"""Read data from the plot source file safely."""
		try:
			with open(self.path, "r") as fp:
				file_data = json.load(fp)
		except FileNotFoundError:
			raise FileNotFoundError(f"Source file not found: {self.path}")
		except json.JSONDecodeError:
			raise ValueError(f"Invalid JSON format in: {self.path}")
		except Exception as e:
			raise RuntimeError(f"Unknown error reading {self.path}: {e}")

		# Now check file_data
		if "data" not in file_data:
			raise ValueError(f"'data' key missing in file: {self.path}")
		if "meta" not in file_data:
			raise ValueError(f"'meta' key missing in file: {self.path}")
		self.data = file_data["data"]
		self.meta = file_data["meta"]
		self.loaded = True


	def clean(self):

		del self.data
		del self.meta
		self.loaded = False

	def get_title(self):
		if(self.loaded == True):

			return self.meta.get("title", "untitled")

	def get_data(self, wants):
		if(self.loaded == True):
			return self.data.get(wants, [])

	def get_xlabel(self):
		if(self.loaded == True):
			return self.meta.get("x_label", "")

	def get_ylabel(self):
		if(self.loaded == True):

			return self.meta.get("y_label", "")

	def get_template_key(self):
		if(self.loaded == True):

			return self.meta.get("template", None)

	def get_legend(self):
		if(self.loaded == True):
			return self.meta.get("legend", "")

