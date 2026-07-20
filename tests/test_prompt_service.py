
from app.core.prompts.service import PromptService


def test_prompt_validation():

    assert PromptService.validate_prompt(
        "hello world"
    ) is True
