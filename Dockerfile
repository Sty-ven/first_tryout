FROM apache/airflow:2.10.0

#use root to install package
USER root

#system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/airflow

COPY requirements.txt .

#Return to airflow user for security
USER airflow

#install python dependencies using pip since that's what you're using
RUN pip --no-cache-dir -r requirements.txt

#Copy DAGs and other necesary files
COPY dags/ /opt/airflow/dags
COPY plugins/ /opt/airflow/plugins
COPY config/ /opt/airflow/config

