
# captcha-api

基于FastAPI + [Captcha Recognizer](https://github.com/chenwei-zhao/captcha-recognizer)库 搭建的滑块验证码识别服务

# 版本要求

* ``Python`` >= 3.8.0

# 依赖包
参考 requirements.txt

# 使用示例

```bash
# 拉取代码
git clone https://github.com/chenwei-zhao/captcha-api

# 进入项目根目录
cd captcha-api

# 安装依赖
pip install -r requirements.txt

# 启动服务
fastapi run

# 测试接口
python api_test.py

```

# 接口文档

启动服务后，在浏览器中访问 ``http://localhost:8000/docs`` 即可查看接口文档。

# Python requests 访问服务示例

```python3
import requests


def test_captcha_api():
    host = 'http://127.0.0.1:8000'
    url = f'{host}/captcha'
    image_path = 'example.png'

    files = {'file': open(image_path, 'rb')}

    data = {'image_type': 'background'}

    response = requests.post(url,
                             data=data,
                             files=files
                             )
    print(f'状态码: {response.status_code}, 响应内容: {response.json()}')


if __name__ == "__main__":
    test_captcha_api()
```

# 其他语言访问服务示例

其他语言请参考接口文档自行编写

# 注意事项

在生产环境中，建议结合Gunicorn和Uvicorn，高效运行FastAPI应用，以提供足够的并发处理能力和稳定性。

# 遇到问题

- Error loading “xxx\Lib\site-packages\torch\lib\fbgemm.dll” or one of its dependencies.
    - 参考 [Issues 2](https://github.com/chenwei-zhao/captcha-recognizer/issues/2)
- Model Unsupported model IR version: 9, max supported IR version: 8
    - 参考 [Issues 1](https://github.com/chenwei-zhao/captcha-recognizer/issues/1)

# 免责声明

本项目不针对任何一家验证码厂商，项目所有内容仅供学习交流使用，严禁用于非法用途。

# 许可证

MIT license

# 联系方式

- Gmail: chenwei.zhaozhao@gmail.com
- 163/网易: chenwei_nature@163.com

# 引用
[1] [Captcha Recognizer](https://github.com/chenwei-zhao/captcha-recognizer)
