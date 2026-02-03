from pydantic import BaseModel, Field


class InferRequest(BaseModel):
    image_path: str = Field(..., description="Local path to image for inference")
    model_version: str = Field("default", description="Model version to use")


class DefectItem(BaseModel):
    label: str
    confidence: float
    bbox: list[float]


class InferResponse(BaseModel):
    model_version: str
    defects: list[DefectItem]
