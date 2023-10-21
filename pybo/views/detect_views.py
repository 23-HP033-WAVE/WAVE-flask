from flask import Blueprint, current_app
import io
from pickletools import read_uint1
from torchvision import models
import json
from flask import Flask, jsonify, request
from flask import make_response
import torchvision.transforms as transforms #pip install torchvision -> pip install opencv-python -> pip install pandas 차례로 필요
import torch
from PIL import Image
import os

bp = Blueprint('detect',__name__, url_prefix='/detect')

# yolo model 불러오기
model = torch.hub.load('./pybo/yolov5', 'custom', path='./pybo/yolov5/runs/train/trash_yolov5l_results4/weights/best.pt', source='local',force_reload=True)


# POST 통신으로 들어오는 이미지를 저장하고 모델로 추론하는 과정
def save_image(file):

    # 저장 디렉토리 생성
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'tmp')

    # 저장 디렉토리가 없으면 생성
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # 파일 저장
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

def s3_get_image_url(s3, filename):
    """
    s3 : 연결된 s3 객체(boto3 client)
    filename : s3에 저장된 파일 명
    """
    location = s3.get_bucket_location(Bucket={'내가 설정한 버킷이름'})["LocationConstraint"]
    return f"https://{{'내가 설정한 버킷이름'}}.s3.{location}.amazonaws.com/{filename}.jpg"

@bp.route('/predict/', methods=['POST'])
def predict():
    if request.method == 'POST':

        #file = request['image'] #url로 변경시켜야합니다
        file=s3_get_image_url('',request['image'])
        save_image(file)  # 들어오는 이미지 저장

        train_img = os.path.join(current_app.config['UPLOAD_FOLDER'], 'tmp')
        train_img = train_img + '/' + file.filename
        temp = model(train_img)
        result = temp.pandas().xyxy[0]['name']
        answer={"바다":0,
                "의류":0,
                "스티로폼":0,
                "다른 배경":0,
                "기타":0,
                "플라스틱":0,
                "나무와 식물":0
                }

        for i in range(len(result)):
            answer[result[i]]+=1



        res={
            "의류":answer["의류"],
            "스티로폼":answer["스티로폼"],
            "기타":answer["기타"],
            "플라스틱":answer["플라스틱"],
        }


    return jsonify(res)

