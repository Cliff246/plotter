def render(ax, plot):
    import numpy as np
    data = np.array(plot.get_data("matrix"))
    cax = ax.matshow(data, cmap='viridis')
    ax.set_title(plot.meta.get("name", "Matrix Plot"))
