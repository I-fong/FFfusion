from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.urls import reverse

from .forms import SimpleUploadForm, ImageUploadForm
from .models import ImageUploadModel
from .utils import cv_swap_face, face_bbox

import requests


class ImageUpload(APIView):
    def get(self, request):
        form = ImageUploadForm()  # GET reuest
        return render(request, 'faceswap/img_upload.html', {'form': form})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            source_image = request.FILES['source_image']

            post.source_image = source_image
            post.save()

            target_image_s3_url = request.POST.get('target_image')
            target_image_content = requests.get(target_image_s3_url).content
            target_image_name = target_image_s3_url.split('/')[-1]
            target_image_path = f"target_images/{target_image_name}"  # 저장될 경로 설정
            default_storage.save(target_image_path, ContentFile(target_image_content))

            upload_image_model = ImageUploadModel.objects.create(
                                                                target_image=target_image_path,
                                                                source_image=source_image
                                                                )

        return redirect(reverse('faceswap:swap_face', kwargs={'id': upload_image_model.id}))


class SwappingFace(APIView):
    target_faces_sorted = None
    source_faces_sorted = None

    def get(self, request, id):
        upload_image_model = ImageUploadModel.objects.get(id=id)
        target_image = upload_image_model.target_image
        source_image = upload_image_model.source_image

        #얼굴 bbox
        target_bbox_list_json, source_bbox_list_json, target_faces_sorted, source_faces_sorted = face_bbox(target_image, source_image)

        SwappingFace.target_faces_sorted = target_faces_sorted
        SwappingFace.source_faces_sorted = source_faces_sorted
    
        context = {
            'target_bbox_json': target_bbox_list_json,
            'source_bbox_json': source_bbox_list_json,
            'img_model': upload_image_model
            }

        return render(request, 'faceswap/faceswap.html', context)
    
    def post(self, request, id):
        upload_image_model = ImageUploadModel.objects.get(id=id)
        target_image = upload_image_model.target_image
        source_image = upload_image_model.source_image

        target_checkboxes = [int(x) for x in request.POST.getlist('target_checkbox')]
        source_checkboxes = [int(x) for x in request.POST.getlist('source_checkbox')]

        result_url = cv_swap_face(target_image,
                                  source_image,
                                  SwappingFace.target_faces_sorted,
                                  SwappingFace.source_faces_sorted,
                                  target_checkboxes,
                                  source_checkboxes[0])  # machine learning

        upload_image_model.result_image = result_url
        
        context = {'swapped_img_url': result_url}

        return render(request, 'faceswap/faceswap.html', context)
        
