from fastapi import FastAPI
from dotenv import load_dotenv
import os

os.environ["ENV_FILE"] = ".env_dev"  # 운영 환경용 파일 지정

load_dotenv(dotenv_path=os.getenv("ENV_FILE"))  # 지정된 환경 파일 로드

from app.main import app
import uvicorn

if __name__ == "__main__":
    ip = os.getenv("IP")
    port_str = os.getenv("PORT")

    if port_str is not None:
        port = int(port_str)
    else:
        port = 8000  # 기본값 설정

    uvicorn.run(app, host=ip, port=port)
