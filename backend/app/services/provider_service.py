
from app.core.models.provider_registry import (
    ProviderRegistry
)

from app.core.models.model_registry import (
    ModelRegistry
)


class ProviderService:

    def get_providers(self):

        return (
            ProviderRegistry
            .list_providers()
        )

    def get_models(
        self,
        provider
    ):

        return (
            ModelRegistry
            .get_models(provider)
        )
