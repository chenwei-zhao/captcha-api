from enum import Enum
from io import BytesIO

import cv2
import numpy as np
from captcha_recognizer.recognizer import Recognizer
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

recognizer = Recognizer()


@app.get("/")
def hello_captcha():
    return {"Hello": "Captcha"}


class ImageType(Enum):
    Background = "background"
    Screenshot = "screenshot"


@app.post("/captcha")
async def create_item(
        image_type: ImageType = Form(..., description="验证码图片类型，background表示单背景图，screenshot表示验证码截图"),
        file: UploadFile = File(...)):
    contents = await file.read()

    # 将字节流转换为numpy数组
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 检查图像是否成功加载
    if image is None:
        return {
            'box': [],
            'confidence': 0,
            "error": "Could not decode image"}

    if image_type == ImageType.Background:
        box, confidence = recognizer.identify_gap(source=image, verbose=False)
    else:
        box, confidence = recognizer.identify_screenshot(source=image, verbose=False)

    return {
        'box': box,
        'confidence': confidence
    }
