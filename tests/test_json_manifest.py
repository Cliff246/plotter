import unittest
from json_manifest import Manifest, Group

class TestManifest(unittest.TestCase):
    def test_manifest_loads(self):
        # Create a dummy manifest file
        import tempfile, json, os

        dummy = {
                "time": "now",
                "manifest_version" : "0.1",
                "origin" : "here",
                "plots": [],
                "plot_groups" : {},
                "graph_path" : "/",
                "render_templates": {},

         }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "manifest.json")
            with open(path, "w") as fp:
                json.dump(dummy, fp)

            m = Manifest(path)
            m.read_manifest()
            self.assertEqual(m.manifest_dict["time"], "now")
            self.assertTrue(m.validate())

if __name__ == "__main__":
    unittest.main()
