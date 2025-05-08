
import os
import watchdog.events
import watchdog.observers
import shutil
import time
import sys


from watchdog.watchdog import ExperimentHandler

def main(base_directory, temp_directory):




	event_handler = ExperimentHandler(temp_directory=temp_directory,dest_directory=base_directory)
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
