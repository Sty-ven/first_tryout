FROM apache/airflow:2.10.0

USER root

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
         build-essential \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set up Python environment
COPY pyproject.toml poetry.lock /opt/airflow/
WORKDIR /opt/airflow

USER airflow

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-ansi

# Copy DAGs and other necessary files
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY config/ /opt/airflow/config/

# Return to airflow user for security
USER airflow

# Update Airflow configuration if needed
# ENV AIRFLOW__CORE__LOAD_EXAMPLES=False