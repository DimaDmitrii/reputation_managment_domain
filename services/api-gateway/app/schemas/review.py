from pydantic import BaseModel

class ReviewCreate(BaseModel):
    author_id: str
    target_id: str
    text: str
    rating: int
    media_ids: list[str] = []