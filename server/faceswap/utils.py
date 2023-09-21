from .apps import FaceswapConfig
import logging
import cv2
from django.conf import settings

from datetime import datetime
import os
from PIL import Image
import numpy as np
import json


def face_bbox(target_image, source_image):
    target_img = cv2.cvtColor(np.array(Image.open(target_image)), cv2.COLOR_RGB2BGR)
    source_img = cv2.cvtColor(np.array(Image.open(source_image)), cv2.COLOR_RGB2BGR)

    target_faces = FaceswapConfig.model.face_detection(target_img)
    source_faces = FaceswapConfig.model.face_detection(source_img)

    target_faces_sorted = sorted(target_faces, key=lambda x: x['bbox'][0])
    source_faces_sorted = sorted(source_faces, key=lambda x: x['bbox'][0])

    target_bbox_list_json = []
    source_bbox_list_json = []

    for target_bbox in target_faces_sorted:
        target_bbox_list_json.append(target_bbox['bbox'].tolist())

    for source_bbox in source_faces_sorted:
        source_bbox_list_json.append(source_bbox['bbox'].tolist())

    target_bbox_list_json = json.dumps(target_bbox_list_json)
    source_bbox_list_json = json.dumps(source_bbox_list_json)

    return target_bbox_list_json, source_bbox_list_json, target_faces_sorted, source_faces_sorted
  

def cv_swap_face(target_image,
                 source_image,
                 target_faces,
                 source_faces,
                 target_checkboxes_list,
                 source_idx):

    target_img = cv2.cvtColor(np.array(Image.open(target_image)), cv2.COLOR_RGB2BGR)
    source_img = cv2.cvtColor(np.array(Image.open(source_image)), cv2.COLOR_RGB2BGR)

    swapped_img_result = None

    for target_idx in target_checkboxes_list:
        if swapped_img_result is None:
            swapped_img_result = FaceswapConfig.model.face_swapping(target_img,
                                                                    source_faces,
                                                                    target_faces,
                                                                    target_idx,
                                                                    source_idx)
        else:
            swapped_img_result = FaceswapConfig.model.face_swapping(swapped_img_result,
                                                                    source_faces,
                                                                    target_faces,
                                                                    target_idx,
                                                                    source_idx)

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    img_name = formatted_datetime+".png"
    result_url = settings.MEDIA_URL + img_name

    cv2.imwrite(settings.MEDIA_ROOT_URL + result_url, swapped_img_result)

    if cv2.imwrite(settings.MEDIA_ROOT_URL + result_url, swapped_img_result):
        print("이미지 저장 성공")
        logging.info("이미지 저장 성공")
    else:
        print("이미지 저장 실패")
        logging.info("이미지 저장 실패")

    return result_url
