from enum import Enum
from io import BytesIO

from captcha_recognizer.recognizer import Recognizer
from fastapi import FastAPI, File, Form, UploadFile
from PIL import Image

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
        image_type: ImageType = Form(..., description="验证码图片类型，background表示背景图，screenshot表示截屏图"),
        file: UploadFile = File(...)):
    file_content = await file.read()
    image_stream = BytesIO(file_content)
    image = Image.open(image_stream)
    if image_type == ImageType.Background:
        box, confidence = recognizer.identify_gap(source=image, verbose=False)
    else:
        box, confidence = recognizer.identify_screenshot(source=image, verbose=False)

    return {
        'box': box,
        'confidence': confidence
    }
