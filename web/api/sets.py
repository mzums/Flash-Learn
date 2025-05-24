from fastapi import APIRouter, Depends, HTTPException
from core.schemas import SetCreate, SetForkCreate, SetResponse
from core.repositories.sets import fork_set, create_set

router = APIRouter(prefix="/sets")


@router.get("/")
def get_sets():
    return {"message": "All sets"}


@router.post("/fork", response_model=SetResponse)
def fork_set_endpoint(fork_data: SetForkCreate):
    return fork_set(fork_data.parent_set_id, fork_data.name, fork_data.is_public)



@router.post("/", response_model=SetResponse)
def create_set_endpoint(set_data: SetCreate):
    try:
        return create_set(creator_id=1, set_data=set_data)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))