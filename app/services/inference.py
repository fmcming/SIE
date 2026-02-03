from app.services.schema import DefectItem, InferRequest, InferResponse


class InferenceService:
    def __init__(self) -> None:
        self.default_model_version = "yolo-stub-v0"

    def infer(self, payload: InferRequest) -> InferResponse:
        # Placeholder inference: return a dummy defect for demo purposes.
        dummy_defect = DefectItem(
            label="scratch",
            confidence=0.01,
            bbox=[0.0, 0.0, 1.0, 1.0],
        )
        return InferResponse(
            model_version=payload.model_version or self.default_model_version,
            defects=[dummy_defect],
        )
