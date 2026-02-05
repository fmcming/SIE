from fastapi import APIRouter
from app.services.inference import InferenceService
from app.services.schema import InferRequest, InferResponse

router = APIRouter()
service = InferenceService()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/infer", response_model=InferResponse)
def infer(payload: InferRequest) -> InferResponse:
    return service.infer(payload)
