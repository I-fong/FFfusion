from django.apps import AppConfig

from .utils import EmbeddingModel


class RecommendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommend'

    model = EmbeddingModel()
