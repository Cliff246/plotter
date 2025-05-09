import json
import os
from json_manifest import Manifest

def validate_scope_dir(path: str) -> bool:
	#TODO
	pass



class Scope:
	"""handles the scope of data"""


	def __init__(self):
		self.path: str = None
		self.scope_key: str = None
		self.scope_obj: dict = None
		self.locked = False

		self.loaded = False
		self.init_manifest = False
		self.manifest_object: Manifest = None


	def validate(self, scope_object: dict):

		if not isinstance(scope_object, dict):
			return False
		prelim_check = [
			"key",
			"manifest_path"
		]
		for prelim in prelim_check:
			if prelim not in scope_object:
				raise ValueError("prelim %s not in scope_object" % prelim)


		##########
		##########
		return



	def load_scope(self, path: str) -> None:
		if(self.locked == False):


			if(validate_scope_dir(path=path) == False):
				self.locked = True
				temp_scope_obj= None
				try:
					with open(path, "r") as fp:
						temp_scope_obj = json.load(fp)
						#after validate we can assume scope_object is fine
						self.validate(scope_object=temp_scope_obj)

				except:
					raise IOError("could not load %s" % path)
				finally:
					self.path: str = path
					self.scope_obj = temp_scope_obj
					self.scope_key = temp_scope_obj["key"]


			else:
				raise RuntimeError("only one scope class can exist for a object")
		else:
			raise ValueError("Locked must equal False")

	def close_scope(self):
		if(self.locked == False):
			raise ValueError("scope must be locked to close")

	def get_manifest_path(self) -> str:
		if(self.locked == True):
			path_to_manifest: str = self.scope_obj["manifest_path"]
			if not isinstance(str, path_to_manifest):
				raise TypeError("manifest path is somehow not a string")
			if(os.path.isfile(path_to_manifest)):
				return path_to_manifest
			else:
				raise IOError("path to manifest %s is not there" % path_to_manifest)
		else:
			raise ValueError("how did you get here? self.locked must be True")



	def get_manifest(self) -> Manifest:

		if(self.locked == True):
			#path should be valid
			if(self.init_manifest == False):
				manifest_path = self.get_manifest_path()

				manifest = Manifest(manifest_path)
				self.init_manifest = True
				self.manifest_object = manifest
				return manifest
			else:
				return self.manifest_object
