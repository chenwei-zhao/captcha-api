from enum import Enum
from typing import List

import cv2
import numpy as np
from captcha_recognizer.recognizer import Recognizer
from captcha_recognizer.slider import SliderV2
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

recognizer = Recognizer()


@app.get("/")
def hello_captcha():
    return {"Hello": "Captcha"}


class VersionEnum(str, Enum):
    V1 = "V1"
    V2 = "V2"


class ImageTypeEnum(str, Enum):
    BACKGROUND = "background"
    SCREENSHOT = "screenshot"


class DetectionResult(BaseModel):
    box: List[int]  # [x1, y1, x2, y2]
    confidence: float
    message: str = None


@app.post("/captcha", response_model=DetectionResult)
async def captcha(
        version: VersionEnum = Form(..., description="验证码版本，V1表示旧版，V2表示新版"),
        image_type: ImageTypeEnum = Form(..., description="验证码图片类型，background表示单背景图，screenshot表示验证码截图"),
        file: UploadFile = File(...)):

    contents = await file.read()

    # 将字节流转换为numpy数组
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        return DetectionResult(box=[], confidence=0, message="不支持的图片")

    if version == VersionEnum.V2:
        box, confidence = SliderV2().identify(source=image)
        # box元素 float转为int
        box = [int(x) for x in box]
        return DetectionResult(box=box, confidence=confidence)
    else:

        if image_type == ImageTypeEnum.BACKGROUND:
            box, confidence = recognizer.identify_gap(source=image, verbose=False)
        else:
            box, confidence = recognizer.identify_screenshot(source=image, verbose=False)

        return DetectionResult(box=box, confidence=confidence)