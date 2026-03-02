from fastapi import APIRouter


router = APIRouter(
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

@router.get("/health")
def health():
    return {"status": "ok"}