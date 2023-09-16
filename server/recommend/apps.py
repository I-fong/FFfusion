from django.apps import AppConfig

from .ml_model import EmbeddingModel


class RecommendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommend'

    model = EmbeddingModel()
