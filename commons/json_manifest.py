import os
import datetime
import time
import json
from plot import *
from templates import Template
from group import Group
from manifest_version import *

class Manifest:
	"""BASE_CLASS"""

	def __init__(self, path: str):

		self.path = path




def init_manifest(path: str) -> Manifest:
	sub_classes: dict[str, Manifest] =	{
		"0.1": JSON_ManifestV1,
		"0.2": JSON_ManifestV2
	}
	try:

		with open(path, "r") as temp:
			temp_manifest_hold = json.load(temp)
			version = temp_manifest_hold["manifest_version"]
			if(version in sub_classes):
				return sub_classes[version](path)
	except:
		raise IOError("could not open manifest %s " % path)
	finally:
		raise ValueError("Manifest Could not be returned")
