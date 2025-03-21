FROM python:3.12

WORKDIR app

RUN pip install wget pyarrow sqlalchemy pandas psycopg2-binary

COPY . .

ENTRYPOINT ["python", "critical.py"]