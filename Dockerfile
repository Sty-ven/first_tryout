FROM python:3.12

WORKDIR /app

RUN pip install wget pandas pyarrow sqlalchemy psycopg2-binary

## Install Poetry
#RUN pip install poetry==1.7.1
#
## Copy poetry configuration files
#COPY pyproject.toml poetry.lock* /app/
#
## Configure poetry to not use a virtual environment
#RUN poetry config virtualenvs.create false
#
## Install dependencies
#RUN poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . /app/

# Run the application
ENTRYPOINT ["python", "critical.py"]