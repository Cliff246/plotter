import matplotlib
matplotlib.use('Agg')  # Force non-interactive backend (good for servers, headless)

import matplotlib.pyplot as plt
from templates import *
from plot import *
from json_manifest import Manifest
from multiprocessing import Process, Queue
import sys
import numpy as np
from logger import setup_logging

def render_worker(manifest, worker_id, shared_queue):
	templates_cache = {}
	setup_logging()

	while True:
		plot = shared_queue.get()
		if plot is None:
			print("shutdown")
			break  # Shutdown signal

		try:
			plot.read_data()
			#print(plot.manifest_info)
			print(f"[Worker {worker_id}] Processing plot: {plot.meta.get('name', 'unknown')}")

			template_key = plot.get_template_key()
			if template_key not in templates_cache:
				template: Template = manifest.templates.get(template_key)
				path = template.look_through_templates_dir()

				if not path:
					raise FileNotFoundError(f"Template for '{template_key}' not found.")

				with open(path, "r") as f:
					local_scope = {"np": np}
					safe_builtins = {
							"__import__": __import__,
							"len": len,
							"range": range,
							"min": min,
							"max": max,
							"abs": abs,
							"sum": sum,
							}
					exec(f.read(), {"__builtins__": safe_builtins}, local_scope)

				render_fn = local_scope.get("render")
				if not callable(render_fn):
					raise ValueError(f"No 'render' function found in {path}.")

				templates_cache[template_key] = render_fn

			render_fn = templates_cache[template_key]

			fig, ax = plt.subplots()
			#print(plot.get_data(plot.meta["type"]))
			render_fn(ax, plot)
			output_path = plot.manifest_info["output"]

			os.makedirs(os.path.dirname(output_path), exist_ok=True)
			plt.savefig(output_path)
			plt.close(fig)
			print(f"[Worker {worker_id}] Finished plot: {plot.meta.get('name', 'unknown')}")
			plot.clean()

		except Exception as e:
			print(f"❌ [Worker {worker_id}] ERROR processing plot {getattr(plot, 'meta', {}).get('name', 'unknown')}: {e}")
			plt.close('all')

		sys.stdout.flush()
		sys.stderr.flush()
	print(f"[Worker {worker_id}] has finished")

def render(manifest: Manifest):

	manifest.read_manifest()
	manifest.load_plots()
	manifest.load_plot_groups()
	manifest.load_templates()
	manifest.fix_paths()

	all_plots = manifest.get_all_plots()
	num_workers = 4 if len(all_plots) >= 4 else len(all_plots)


	# Simple round-robin dispatcher
	current = 0

	shared_queue = Queue()
	for plot in all_plots:
		shared_queue.put(plot)

	workers = []

	for i in range(num_workers):
		p = Process(target=render_worker, args=(manifest, i, shared_queue))
		p.start()
		workers.append(p)

	for _ in range(num_workers):
		shared_queue.put(None)

	for p in workers:
		p.join(timeout=1000)  # wait 60 seconds max per worke
		if p.is_alive():
			print(f"❌ Worker {p.pid} is still alive after timeout. Dying in fire.", level="ERROR")
			raise RuntimeError(f"🔥 Worker {p.pid} failed to terminate in time. SYSTEM PANIC. 🔥")
