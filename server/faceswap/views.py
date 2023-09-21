from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import SimpleUploadForm, ImageUploadForm
from .models import ImageUploadModel
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .utils import cv_swap_face, face_bbox
from .apps import FaceswapConfig
from PIL import Image
import numpy as np
import json
import pickle
from rest_framework.views import APIView


class ImageUpload(APIView):
    def get(self, request):
        form = ImageUploadForm()  # GET reuest
        return render(request, 'faceswap/img_upload.html', {'form': form})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)            
            target_image = request.FILES['target_image']
            source_image = request.FILES['source_image']
            post.target_image = target_image
            post.source_image = source_image
            ###
            post.save()  # DB에 실제로 form 객체('form')에 채워져 있는 데이터를 저장

            target_url = settings.MEDIA_URL + form.instance.target_image.name
            source_url = settings.MEDIA_URL + form.instance.source_image.name
            # 실제로 db에 저장되어있는 경로 '/media/images/2021/07/30/image.jpg'

            # 저장된 이미지를 가져오기
            upload_image_model = ImageUploadModel.objects.create(
                target_image=target_image, source_image=source_image
                )
            # reverse 함수를 사용하여 URL을 생성하고 해당 URL로 리다이렉트
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
        
