from pydantic import BaseModel

class requestDTO(BaseModel):
    video_link: str

    class Config:
        extra = 'forbid'