import requests


def test_captcha_api():
    host = 'http://127.0.0.1:8000'
    url = f'{host}/captcha'
    image_path = 'example.png'

    files = {'file': open(image_path, 'rb')}

    data = {'image_type': 'background', 'version': 'V2'}

    response = requests.post(url,
                             data=data,
                             files=files
                             )
    print(f'状态码: {response.status_code}, 响应内容: {response.json()}')


if __name__ == "__main__":
    test_captcha_api()
