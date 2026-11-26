FROM python:3.14-alpine

WORKDIR app

RUN pip install --no-cache-dir python-dotenv flask-sqlalchemy pymysql cryptography

COPY . .

CMD ["python", "run.py"]
