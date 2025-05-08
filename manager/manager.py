import os
import watchdog.events
import watchdog.observers
import shutil
import time
import sys

from commons.json_manifest import Manifest
from renderer.plot_renderer import render
from watchdog.watchdog import ExperimentHandler
import collections
import os
import datetime
DEBUG = 0

def wait_for_sources(manifest, timeout=10):
	"""Wait until all source files in the manifest exist or timeout."""
	start_time = time.time()
	while time.time() - start_time < timeout:
		missing = []
		for plot in manifest.plots:
			if not os.path.exists(plot.path):
				missing.append(plot.path)
		if not missing:
			return True
		time.sleep(0.5)  # Short intelligent wait, not blind
	raise RuntimeError(f"Timeout: Missing files: {missing}")
