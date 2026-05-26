from pydantic import BaseModel


class FileWriteRequest(BaseModel):
    filepath: str
    content: str
    overwrite: bool = False
    append: bool = False
