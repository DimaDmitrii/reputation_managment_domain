from pydantic import BaseModel

class MediaUploadCreate(BaseModel):
    filename: str
    size: int
    content_type: str


