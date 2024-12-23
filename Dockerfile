# Python 3.9-slim 이미지를 사용
FROM python:3.9-slim

# 작업 디렉토리를 /app으로 설정
WORKDIR /app

# requirements.txt 파일을 컨테이너에 복사
COPY requirements.txt .

# requirements.txt에 명시된 Python 패키지들을 설치
RUN pip install --no-cache-dir -r requirements.txt

# 현재 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리에 복사
COPY . .

# Uvicorn을 사용하여 FastAPI 애플리케이션을 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 컨테이너가 8000번 포트를 열도록 설정
EXPOSE 8000