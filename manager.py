import os
import watchdog.events
import watchdog.observers
import shutil
import time
import sys
from json_manifest import Manifest
from plot_renderer import render
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

def main(base_directory, temp_directory):
	class ExperimentHandler(watchdog.events.FileSystemEventHandler):

		def __init__(self):
			self.running = False
			self.event_queue = collections.deque()
			super().__init__()

		def on_any_event(self, event):
			if(DEBUG==1):	
				print("event", event)
			try:
				self.event_queue.append(event)
				self.process_queue()
			except Exception as e:
				print(f"❌ Watchdog handler error in on_moved: {e}", level="ERROR")



		def process_queue(self):
			if not self.running and self.event_queue:
				#print("proccess queue")
				event = self.event_queue.popleft()
				try:
					self.process_experiment(event)
				finally:
					self.running = False
					self.process_queue()  # Immediately check and process next event

		def process_experiment(self, event):
			#print(event)
			if event.is_directory and self.running == False :
				self.running = True
				try:
					experiment_path = event.src_path
					if not os.path.exists(experiment_path):
						return False
					manifest_path = os.path.join(experiment_path, "manifest.json")
					# Wait until manifest.json appears or timeout
					timeout = 5
					waited = 0
					# Only process if the event is a direct child of the watch folder
					if os.path.dirname(event.src_path) != temp_directory:
						return False # Ignore nested subdirectories
					while not os.path.exists(manifest_path) and waited < timeout:
						time.sleep(1)
						waited += 1
					if not os.path.exists(manifest_path):
						print(f"❌ ERROR: Manifest not found in {experiment_path}, skipping.")
						return False
					experiment_name = os.path.basename(experiment_path)
					date = datetime.datetime.now()
					date_directory = "%s_%s_%s" % (date.day, date.month, date.year) 
					sub_directory = os.path.join(base_directory, date_directory)

					os.makedirs(sub_directory, exist_ok=True)

					base_experiment_path = os.path.join(sub_directory, experiment_name)
					plots_path = os.path.join(base_experiment_path, "plots")
					data_path = os.path.join(base_experiment_path, "data")
					meta_path = os.path.join(base_experiment_path, "meta")
					os.makedirs(plots_path, exist_ok=True)
					os.makedirs(data_path, exist_ok=True)
					os.makedirs(meta_path, exist_ok=True)
					# Copy raw data files and folders to data/ (except manifest.json)
					for item in os.listdir(experiment_path):
						if item == "manifest.json":
							continue
						src_item = os.path.join(experiment_path, item)
						dest_item = os.path.join(data_path, item)
						if os.path.isdir(src_item):
							shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
						else:
							shutil.copy2(src_item, dest_item)

					try:
						manifest = Manifest(manifest_path, base_experiment_path)
						manifest.read_manifest()
						wait_for_sources(manifest, 10)
						render(manifest)
						print(f"✅ Rendering plots for experiment {experiment_name} into {plots_path}")
						print(f"✅ Experiment {experiment_name} processed successfully.")

						# After rendering succeeds, copy manifest separately
						shutil.copy2(manifest_path, os.path.join(base_experiment_path, "manifest.json"))

						# Now cleanup RAM folder
						shutil.rmtree(experiment_path)
						return True

					except:
						print(f"❌ rendering failed")
						return False


				except Exception as e:
					print(f"❌ CRITICAL FAILURE while processing {event.src_path}: {e}")
					os._exit(1)
				finally:
					self.running = False




	event_handler = ExperimentHandler()
	observer = watchdog.observers.Observer()
	observer.schedule(event_handler, path=temp_directory, recursive=False)
	observer.start()
	print(f"Watching {temp_directory} for new experiment folders...")
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	except Exception as e:
		print(f"❌ CRITICAL SYSTEM FAILURE: {e}", level="ERROR")
		import traceback
		traceback.print_exc()
		raise RuntimeError(f"🔥 SYSTEM PANIC: {e} 🔥")
	observer.join()
