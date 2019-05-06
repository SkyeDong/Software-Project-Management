# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import random
from app import models
from plugins.music_dl.__main__ import Music

import cv2
from keras.models import model_from_json
from PIL import Image, ImageTk
import numpy as np
import keras
import pandas as pd
import time

global emotion  # 首次声明全局变量
emotion = ''
global init
init = 0

# 首页
def index(req):
    global init
    init = 0
    # 将数据传递给模板,模板再渲染页面，将渲染好的页面返回给浏览器
    return render(req, 'index_player.html')


# 表情识别页面
def index_emotion(req):
    global init
    if init == 0:
        init = init + 1
        return render(req, 'index_emotion_init.html')
    else:
        return render(req, 'index_emotion.html')


# 从前端获取选择图片,保存到指定路径
def get_url(req):
    # 从前端获取选择图片,保存到指定路径
    myFile = req.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
    if not myFile:
        return HttpResponse("no files for upload!")
    destination = open(os.path.join("./upload/", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    # 表情识别
    emotion_url="./upload/"+ myFile.name
    global emotion  # 为了说明使用的是全局变量
    emotion = get_emotion(emotion_url)
    print(emotion)
    recommend_songs(req)

    return HttpResponse('success')

# 刷新页面
def return_emotion(req):
    global emotion

    print(999)
    print(emotion)
    resp = {'emotion': emotion}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def get_emotion(str):
    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'normal']
    faceCascade = cv2.CascadeClassifier('D:/django_songs-master/app/haarcascade_frontalface_default.xml')  # Opencv中做人脸检测的时候的一个级联分类器
    # 加载json并且创建模型拱门
    json_file = open('D:/django_songs-master/app/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    keras.backend.clear_session()
    model = model_from_json(loaded_model_json)  # keras载入model
    model.load_weights('D:/django_songs-master/app/model.h5')  # 加载权重到新的模型中

    def overlay_memeface(probs):
        emotion = emotion_labels[np.argmax(probs)]  # 找评分最高的作为label
        return emotion

    def predict_emotion(face_image_gray):  # a single cropped face
        resized_img = cv2.resize(face_image_gray, (48, 48), interpolation=cv2.INTER_AREA)
        # 先把灰度人脸用插值法转化为48*48大小
        # 基于局部像素的重采样，对于图像抽取来说，是更好的方法
        # cv2.imwrite(str(index)+'.png', resized_img)
        image = resized_img.reshape(1, 48, 48, 1)
        list_of_list = model.predict(image, batch_size=1, verbose=1)
        angry, disgust, fear, happy, sad, surprise, normal = [prob for lst in list_of_list for prob in lst]
        return [angry, disgust, fear, happy, sad, surprise, normal]

    im = Image.open(str)  # 打开选择的图像
    frame = np.array(im)  # 将image读取到的照片转换为数组格式

    r, g, b = cv2.split(frame)
    frame = cv2.merge([b, g, r])  # cv2遵循[B,G,R],而python的PIL读取到的图片为[R,G,B],所以进行数组转换

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, 1)  # 转化为灰度图片（灰度图像加快检测速度）

    faces = faceCascade.detectMultiScale(  # opencv2中人脸检测使用的是 detectMultiScale函数。它可以检测出图片中所有的人脸，并将人脸用vector保存各个人脸的坐标、大小（用矩形表示）
        img_gray,  # 待检测图像
        scaleFactor=1.2,  # 表示在前后两次相继的扫描中，搜索窗口的比例系数。默认为1.1即每次搜索窗口依次扩大10%
        minNeighbors=5,
        minSize=(30, 30)
    )
    # 表情画框
    for (x, y, w, h) in faces:
        face_image_gray = img_gray[y:y + h, x:x + w]  # 灰度人脸
        face_image = frame[y:y + h, x:x + w]  # 彩图人脸

        # 从emotion列表中找评分最高的emotion作为emotion
        emotion = overlay_memeface(predict_emotion(face_image_gray))
    return emotion

def recommend_songs(req):
    global emotion  # 为了说明使用的是全局变量
    print(emotion)
    csv_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/music.csv"))  # 音乐库的绝对路径
    musicdata = pd.read_csv(csv_path)  # 音乐库
    recommend_list = musicdata[musicdata['label']==emotion]['music'].tolist()  # label=emotion的所有音乐文件名的列表
    name_or_singer = [song.replace(".mp3", '').split('-') for song in recommend_list]  # [['歌手','歌曲'],...]

    list = [name for name in name_or_singer if len(name) < 3]  # [['歌手','歌曲'],...]
    rspid = [i + 1 for i in range(len(list))]  # 为每首歌编号1，2，。。。
    name = [name[1].strip() for name in list]  # 每首歌对应的歌曲列表
    singer = [name[0].strip() for name in list]  # 每首歌对应的歌手列表
    songs = ["-".join(song) + ".mp3" for song in list]  # ['歌手 - 歌曲.mp3',...]

    # 为每首歌随机分配封面图片
    bgp_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/images/"))  # 歌曲封面的绝对路径
    bgp_file = os.listdir(bgp_path)  # 封面图片文件名列表
    bgp = []
    for i in range(len(songs)):
        bgp.append(bgp_file[random.randint(0, len(bgp_file) - 1)])

    # 歌曲字典列表[{'respid':编号, 'songs':歌曲文件名.mp3, 'bgp':封面图片文件名, 'name':歌名, 'singer':歌手},...]
    resp_data = []
    for i in range(len(rspid)):
        resp_data.append({
            "rspid": rspid[i],
            "songs": songs[i],
            "bgp": bgp[i],
            "name": name[i],
            "singer": singer[i]
        })
    resp = {'status_code': 200, 'data': resp_data}
    return HttpResponse(json.dumps(resp), content_type="application/json")



def get_songs(req):
    # 遍历songs目录, 获取所有歌曲文件名并区分歌曲名与歌手名
    songs_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/songs/"))  # 音乐库的绝对路径
    songs_list = os.listdir(songs_path)  # 该路径下歌曲文件列表
    name_or_singer = [song.replace(".mp3", '').split('-') for song in songs_list]  # [['歌手','歌曲'],...]

    list = [name for name in name_or_singer if len(name) < 3]  # [['歌手','歌曲'],...]
    rspid = [i + 1 for i in range(len(list))]  # 为每首歌编号1，2，。。。
    name = [name[1].strip() for name in list]  # 每首歌对应的歌曲列表
    singer = [name[0].strip() for name in list]  # 每首歌对应的歌手列表
    songs = ["-".join(song) + ".mp3" for song in list]  # ['歌手 - 歌曲.mp3',...]


    # 为每首歌随机分配封面图片
    bgp_path = os.path.realpath(os.path.join(__file__, "../../static/music_data/images/"))  # 歌曲封面的绝对路径
    bgp_file = os.listdir(bgp_path)  # 封面图片文件名列表
    bgp = []
    for i in range(len(songs)):
        bgp.append(bgp_file[random.randint(0, len(bgp_file) - 1)])


    # 歌曲字典列表[{'respid':编号, 'songs':歌曲文件名.mp3, 'bgp':封面图片文件名, 'name':歌名, 'singer':歌手},...]
    resp_data = []
    for i in range(len(rspid)):
        resp_data.append({
            "rspid": rspid[i],
            "songs": songs[i],
            "bgp": bgp[i],
            "name": name[i],
            "singer": singer[i]
        })
    resp = {'status_code': 200, 'data': resp_data}
    return HttpResponse(json.dumps(resp), content_type="application/json")


music_dic = {}


def search_songs(req):
    if req.method == 'POST':
        music_dic['music'] = Music()
        req_data = req.POST
        song_name = req_data.get('song_name')
        resp_data = music_dic['music'].search(song_name)
        # resp_data = [song_name]
        status_code = 200
    elif req.method == 'GET':
        idx = req.GET.get('idx', default='0')
        music_dic['music'].downlod_songs(idx)
        resp_data = ['下载成功']
        status_code = 200
    else:
        resp_data = ['123']
        status_code = 400
    resp = {'status_code': status_code, 'data': resp_data}
    return HttpResponse(json.dumps(resp), content_type="application/json")



if __name__ == '__main__':
    print(get_songs(111))
