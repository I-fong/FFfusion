from django.apps import AppConfig
from swapmodel.ml_models import FaceSwapModel


class FaceswapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faceswap'

    model = FaceSwapModel()
