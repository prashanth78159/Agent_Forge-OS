
from app.core.models.model_registry import (
    ModelRegistry
)


class ModelRouterService:

    def get_models(
        self,
        provider
    ):

        return ModelRegistry.get_models(
            provider
        )

    def default_model(
        self,
        provider
    ):

        models = self.get_models(
            provider
        )

        return models[0] if models else None
