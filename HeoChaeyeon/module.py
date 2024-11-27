#----------------------------------------------#
# 필요한 module
import tensorflow as tf
import numpy as np
import os
from PIL import Image

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
#----------------------------------------------#
# web에 올라온 image
def upload_image(uploaded_file):

    # 저장 경로 설정
    SAVE_DIR = "upload_img"
    os.makedirs(SAVE_DIR, exist_ok=True)

    # 이미지 준비
    # uploaded_file은 UploadedFile 객체이다. # > app.py에서 선언하고 함수 호출 시에 넘겨 줘야함
    IMAGE_SIZE = 224
    image = Image.open(uploaded_file)  # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1500x1500 at 0x198B95F8250>
    image_np = np.array(image)

    # cv2 대신 tf.image.resize 사용
    resized_image = tf.image.resize(image_np, (IMAGE_SIZE, IMAGE_SIZE))
    a_image = np.array(resized_image)
    # MobileNetV2 전용 스케일링
    a_image = preprocess_input(a_image)
    batch_image = a_image.reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3)

    # 서버에 저장
    save_path = os.path.join(SAVE_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return batch_image
#----------------------------------------------#
# settind : 최적의 model 불러오고, class_name과 class_explain 선언
def setting():
    # 모델 로드 및 예측
    filepath = 'best_cloud_mobilenet.keras'
    model = load_model(filepath)
    class_name="['난층운','적란운'...]" ## sample folder에서
    class_explain="['난층운의 특징',...]"
    return model,class_name,class_explain
#----------------------------------------------#
# test_accuracy : 웹에 업로드된 사진 분류 진행!
def test_accuracy(uploaded_file):
    batch_image=upload_image(uploaded_file)
    model, class_name, class_explain = setting()
    pred_proba = model.predict(batch_image)

    pred = np.argmax(pred_proba)
    pred_label = class_name[pred]
    pred_description = class_explain[pred]
    images_name=class_sample_image(pred_label)

    return pred, pred_label, pred_description,images_name
#----------------------------------------------#
# class_sample_image : 해당 구름 sample 이미지!
def class_sample_image(pred_label):
    # 근데 이게 영어로 들어와야되는데 저거는 난층운 ~ 요따구란 말이지
    # 그래서 여기 수정 필요함 일단 이렇게
    filepath = f'./cloud_img/sample_cloud_img/{pred_label}'
    image_names = []
    try:
        for file_name in os.listdir(filepath):
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_names.append(file_name)
    except FileNotFoundError:
        print(f"Error: Directory '{filepath}' does not exist.")
    return image_names
