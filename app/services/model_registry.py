from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ModelInfo:
    name: str
    version: str
    task: str = "defect-detection"
    framework: str = "yolo"


class ModelRegistry:
    """Placeholder model registry for future integration."""

    def __init__(self) -> None:
        self._default = ModelInfo(name="yolo-stub", version="v0")

    def resolve(self, version: Optional[str]) -> ModelInfo:
        if version:
            return ModelInfo(name="yolo-stub", version=version)
        return self._default
