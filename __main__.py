
import sys
import os
from logger import setup_logging

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from manager import main

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python manager.py <base_directory> <temp_directory>")
		sys.exit(1)
	print("start")
	main(sys.argv[1], sys.argv[2])
