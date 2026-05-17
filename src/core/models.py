from pydantic import BaseModel, AnyHttpUrl
from typing import Optional, List

class KnowledgeTripletItem(BaseModel):
    item: str
    info: str = ''
    # Use pydantic url type for validation
    url: AnyHttpUrl = ''
    type_: List[str] = []

class KnowledgeTriplet(BaseModel):
    subject: KnowledgeTripletItem
    object: KnowledgeTripletItem
    relation: KnowledgeTripletItem