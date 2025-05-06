
def render(ax, plot):
	import numpy as np
	"""
	Render a 2D line plot on the given axis (ax).

	Parameters:
	ax -- The matplotlib axis to draw on
	plot -- The Plot object containing the plot data
	"""

	# Extract data
	x_data = np.array(plot.get_data("points"))  # First row as X data
	y_data = np.arange(len(x_data))
	# Plot the line
	ax.plot(y_data, x_data, label=plot.meta.get("name", "Line Plot"), color='b')

	# Set title and labels
	ax.set_title(plot.meta.get("name", "Line Plot"))
	ax.set_xlabel("X-axis")
	ax.set_ylabel("Y-axis")

	# Optionally, add a grid
	ax.grid(True)

	# Optionally, add a legend
	ax.legend()
