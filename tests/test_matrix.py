import unittest
import os
import json
from json_manifest import Manifest
from plot import Plot
from plot_renderer import render

class TestRenderFlow(unittest.TestCase):

	def setUp(self):
		self.test_root = "tests/dummy_tests/"
		self.manifest_path = os.path.join(self.test_root, "manifest.json")

	def test_manifest_loads(self):
		manifest = Manifest(self.manifest_path)
		manifest.read_manifest()
		self.assertIn("plots", manifest.manifest_dict)
		self.assertGreater(len(manifest.manifest_dict["plots"]), 0)

	def test_main(self):
		manifest = Manifest(self.manifest_path)
		manifest.read_manifest()
		render(manifest)


if __name__ == "__main__":
	#unittest.main()
	pass