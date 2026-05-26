from pydantic import BaseModel


class FileAnalysisRequest(BaseModel):
    filepath: str
