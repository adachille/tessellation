"""Base class for tesselation generators."""

import json
from pathlib import Path
from typing import Optional, Any, Union

import numpy as np

from tessellation.procgen.tessellation_type import TessellationType


class GenerationResult:
    def __init__(
        self,
        mask: np.ndarray,
        tessellation_type: TessellationType,
        metadata: Optional[dict] = None,
    ):
        self.mask = mask
        self.tessellation_type = tessellation_type
        self.metadata = metadata or {}

    def save_as_json(self, file_path: Union[Path, str]):
        """Save the generation result as a JSON file."""
        with open(file_path, "w") as file:
            json.dump(self.to_json(), file, indent=2)

    def to_json(self) -> dict[str, Any]:
        """Return the generation result as a JSON serializable dictionary."""
        return {
            "tessellation_type": self.tessellation_type.value,
            "mask": self.mask.tolist(),
            "metadata": {**self.metadata},
        }
