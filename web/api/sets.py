from fastapi import APIRouter, Depends
router = APIRouter(prefix="/sets")

@router.get("/")
def get_sets():
    return {"message": "All sets"}