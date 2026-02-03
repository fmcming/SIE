import time
from pathlib import Path

from fastapi import HTTPException

from app.core.config import settings
from app.services.model_registry import ModelRegistry
from app.services.schema import DefectItem, InferRequest, InferResponse


class InferenceService:
    def __init__(self) -> None:
        self.registry = ModelRegistry()

    def infer(self, payload: InferRequest) -> InferResponse:
        start_time = time.perf_counter()
        image_path = Path(payload.image_path)
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image path not found")

        model = self.registry.resolve(payload.model_version)
        # Placeholder inference: return a dummy defect for demo purposes.
        dummy_defect = DefectItem(
            label="scratch",
            confidence=0.01,
            bbox=[0.0, 0.0, 1.0, 1.0],
        )
        duration_ms = (time.perf_counter() - start_time) * 1000
        return InferResponse(
            image_path=str(image_path),
            model_version=model.version or settings.default_model_version,
            defects=[dummy_defect],
            duration_ms=duration_ms,
        )
