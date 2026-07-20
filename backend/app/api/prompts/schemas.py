
from pydantic import BaseModel


class CreatePromptRequest(BaseModel):

    name: str

    description: str

    category: str

    prompt: str
