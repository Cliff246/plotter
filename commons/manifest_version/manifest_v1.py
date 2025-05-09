from commons.json_manifest import *



class JSON_ManifestV1(Manifest):

	

	def __init__sub(self, path):

		super.__init__( self, path)
		self.plots: list[Plot] = []
		self.groups: dict[str, Group] = {}
		self.content: dict  = {}
		self.manifest_dict: dict = {}
		self.load_date = datetime.datetime.now().strftime("run_%Y%m%d_%H%M%S")
		self.load_time = time.time()
		self.subfolders: set[str] = set()
		self.has_read = False
		self.templates: dict[str, Template]  = {}


	def get_all_plots(self) -> list[Plot]:

		all_plots = []

		all_plots.extend(self.plots)

		for key, value in self.groups.items():
			if(isinstance(value, Group)):
				all_plots.extend(value)
		return all_plots

	def validate(self) -> bool:
		required_elements = [
			"time",
			"manifest_version",
			"origin",
			"plots",
			"plot_groups",
			"graph_path",
			"render_templates",
		]


		all_good = True
		#print(self.manifest_dict)
		for elem in required_elements:
			if(elem not in self.manifest_dict.keys()):

				raise ValueError("%s not in manifest" % elem)
		return all_good

	def read_manifest(self):
		"""Reads and validates the manifest file."""
		try:
			with open(self.path, "r") as fp:
				self.manifest_dict = json.load(fp)
		except FileNotFoundError:
			raise FileNotFoundError(f"Manifest file not found: {self.path}")
		except json.JSONDecodeError as e:
			raise ValueError(f"Manifest file is not valid JSON: {self.path} ({e})")
		except Exception as e:
			raise RuntimeError(f"Unexpected error opening manifest {self.path}: {e}")

		try:
			if not self.validate():
				raise ValueError(f"Manifest validation failed: {self.path}")
		except Exception as e:
			raise ValueError(f"Error validating manifest {self.path}: {e}")

		self.has_read = True


	def create_subfolders(self):

		"""Create necessary subfolders inside plots/ and data/ based on groups."""
		#TODO
		plots_base = os.path.join(, "plots")
		data_base = os.path.join(, "data")

		for sub in self.subfolders:
			try:
				os.makedirs(os.path.join(plots_base, sub), exist_ok=True)
				os.makedirs(os.path.join(data_base, sub), exist_ok=True)
			except Exception as e:
				raise OSError(f"could not create subfolders {sub}: {e}")
	def load_plots(self):
		if(self.has_read == True):
			for elem in self.manifest_dict["plots"]:
				plot = Plot(elem)
				self.plots.append(plot)
			return
		else:
			print("has not read the manifest yet")
			return


	def get_group_from_key(self, group_key) -> Group:
		if(group_key not in self.manifest_dict["plot_groups"]):
			raise ValueError("group key not in manifest")

		group = self.manifest_dict["plot_groups"][group_key]
		meta = group["meta"]
		content = []


		for elem in group["plots"]:
			content.append(Plot(elem))

		ret = Group(group_key, meta, content)
		return ret


	def load_plot_groups(self):
		if(self.has_read == True):

			plot_groups =  self.manifest_dict["plot_groups"]

			for key, value in plot_groups.items():
				self.groups[key] = self.get_group_from_key(key)
				self.subfolders.add(key)

		else:
			raise ValueError("has read = False")

		for key in self.groups.keys():

			load_group: list[dict] = self.groups[key].contents
			#print(key, load_group)
			#print()
			for elem in load_group:
				self.plots.append(elem)


	def load_templates(self):


		manifest_templates: dict = self.manifest_dict["render_templates"]
		for key, value in manifest_templates.items():


			temp = Template(key, value)

			self.templates[key] = temp

	def fix_output_paths(self):
		"""Fix plot output paths dynamically based on group or single status."""

		# Fix plots in normal plot list
		for plot in self.plots:
			plot_basename = os.path.basename(plot.manifest_info["output"])  # e.g., "weight0.png"

			# Place into Singles folder
			plot.manifest_info["output"] = os.path.join(, "plots", "Singles", plot_basename)

		# Fix plots in groups
		for group_key, group in self.groups.items():
			for plot in group:
				plot_basename = os.path.basename(plot.manifest_info["output"])  # e.g., "weight0.png"
				plot.manifest_info["output"] = os.path.join(, "plots", group_key, plot_basename)


	def fix_data_paths(self):
		"""Fix raw data output paths to match plots."""
		for plot in self.plots:
			data_basename = os.path.basename(plot.manifest_info["source"])
			new_path = os.path.join(, "data", "Singles", data_basename)
			plot.manifest_info["source"] = new_path
			plot.path = new_path

		for group_key, group in self.groups.items():
			for plot in group:
				data_basename = os.path.basename(plot.manifest_info["source"])
				new_path = os.path.join(, "data", group_key, data_basename)
				plot.manifest_info["source"] = new_path
				plot.path = new_path

	def fix_paths(self):

		self.fix_output_paths()
		self.fix_data_paths()

		#for pth in self.get_all_plots():
			#print(pth.manifest_info)
