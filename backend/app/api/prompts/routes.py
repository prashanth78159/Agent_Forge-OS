
from fastapi import APIRouter

from app.core.prompts.service import PromptService

router = APIRouter(
    prefix="/api/prompts",
    tags=["Prompt Studio"]
)

service = PromptService()


@router.get("/")
def list_prompts(
    user_id: str
):

    return service.list_prompts(
        user_id
    )


@router.get("/{prompt_id}")
def get_prompt(
    prompt_id: str
):

    return service.get_prompt(
        prompt_id
    )
