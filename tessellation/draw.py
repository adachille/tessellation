"""Drawing module."""

from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import numpy as np


class Drawer:
    """Drawer class."""

    def draw(self, *args, **kwargs):
        """Draw the tessellation."""
        raise NotImplementedError


class MPLDrawer(Drawer):
    """Matplotlib drawer class."""

    def __init__(self, cmap: str = "binary"):
        self.cmap = cmap

    def draw(self, tessellation: np.ndarray):
        """Draw the tessellation."""
        plt.imshow(tessellation, cmap=plt.get_cmap(self.cmap))

    def save_as_png(self, file_path: Union[Path, str], tessellation: np.ndarray):
        """Save the drawing as a PNG file."""
        plt.imsave(file_path, tessellation, cmap=plt.get_cmap(self.cmap))
