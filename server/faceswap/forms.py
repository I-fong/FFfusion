from django import forms
from .models import ImageUploadModel


# simple upload form
class SimpleUploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    image = forms.ImageField()  # file field + image


# description 추가
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('source_image', )
