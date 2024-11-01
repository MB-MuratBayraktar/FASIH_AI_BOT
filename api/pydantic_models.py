from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class ModelName(str, Enum):
    GPT35_TURBO = "gpt-3.5-turbo-0125"
    BABBAGE = "babbage-002"
    GPT35_TURBO_INSTRUCT = "gpt-3.5-turbo-instruct"

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT35_TURBO)

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime


class Document(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int
