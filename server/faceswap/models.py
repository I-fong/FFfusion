from django.db import models


class ImageUploadModel(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.ImageField(upload_to='images/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    target_image = models.ImageField(upload_to='target_images/')
    source_image = models.ImageField(upload_to='source_images/')
    result_image = models.ImageField(upload_to='result_images/%Y/%m/%d', blank=True, null=True)