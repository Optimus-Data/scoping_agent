from pydantic import BaseModel
from typing import Optional

class BudgetSearchRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None
