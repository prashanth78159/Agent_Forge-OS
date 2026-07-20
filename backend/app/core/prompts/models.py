
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PromptTemplate:
    id: Optional[str]
    user_id: str

    name: str
    description: str

    category: str

    prompt: str

    version: int = 1

    status: str = "DRAFT"

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
