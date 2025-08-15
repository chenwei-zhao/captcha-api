# captcha-api

基于Vue + FastAPI 搭建的验证码识别演示平台
验证码识别库:  [Captcha Recognizer](https://github.com/chenwei-zhao/captcha-recognizer)

# 依赖

## 前端

参考 package.json

# 后端
参考 requirements.txt

# 启动前端UI

```shell
cd frontend
npm install
npm run dev/build
```

# 启动后端服务

```shell
cd backend
pip install -r requirements.txt
uvicorn main:app --port 8000
```

# 注意事项

在生产环境中，建议结合Gunicorn和Uvicorn，高效运行FastAPI应用，以提供足够的并发处理能力和稳定性。

# 许可证

MIT license

# 联系方式

- Gmail: chenwei.zhaozhao@gmail.com
- 163/网易: chenwei_nature@163.com

# 引用

[1] [Captcha Recognizer](https://github.com/chenwei-zhao/captcha-recognizer)
