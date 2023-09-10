from flask import Blueprint, url_for, render_template, flash, request, session, g
import io
from pickletools import read_uint1
from torchvision import models
import json
from flask import Flask, jsonify, request
from flask import make_response
import torchvision.transforms as transforms #pip install torchvision 필요합니다
import torch
from PIL import Image
import os

bp=Blueprint('detect',__name__, url_prefix='/detect')

# yolo model 불러오기
model = torch.hub.load('./yolov5/', 'custom', path='./yolov5/runs/train/trash_yolov5l_results4/weights/best.pt', source='local')

# POST 통신으로 들어오는 이미지를 저장하고 모델로 추론하는 과정
def save_image(file):
    file.save('./temp/'+ file.filename)

@bp.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        save_image(file)  # 들어오는 이미지 저장
        train_img = './temp/' + file.filename
        temp = model(train_img)
        result = temp.pandas().xyxy[0]['name']
        answer={}

        for i in range(len(result)):
            answer[result[i]]+=1

        res={
            answer
        }
        return res

