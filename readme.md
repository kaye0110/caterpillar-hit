# 环境准备

# 启动项目
```shell
pipenv shell
nohup uvicorn --workers 2 --port 19999 --env-file .env app.application:app > nohup.out 2>&1 &
```

