# Use official Apache Airflow image
FROM apache/airflow:2.10.5

# Use root to install OS packages
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    build-essential \
 && apt-get autoremove -yqq --purge \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/airflow

# Copy Python requirements file
COPY requirements.txt .

# Switch to airflow user BEFORE installing Python packages
USER airflow

# Install Python dependencies using pip (as airflow user)
RUN pip install --no-cache-dir -r requirements.txt

# Copy your DAGs, plugins, and configs
COPY --chown=airflow:airflow dags/ /opt/airflow/dags/
COPY --chown=airflow:airflow plugins/ /opt/airflow/plugins/
COPY --chown=airflow:airflow config/ /opt/airflow/config/
