FROM python:3.9

WORKDIR /test_task

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn","app.main:app","--bind=0.0.0.0:8888"]