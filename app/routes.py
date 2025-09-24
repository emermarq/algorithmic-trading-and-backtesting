from fastapi import APIRouter

router = APIRouter()

@router.get("/items")
def get_items():
    return [{"item_id": 1}, {"item_id": 2}]