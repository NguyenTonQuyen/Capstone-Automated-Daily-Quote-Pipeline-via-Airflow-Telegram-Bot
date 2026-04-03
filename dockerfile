# FROM apache/airflow:latest

# USER root
# RUN apt-get update && \
#     app-get -y install git && \
#     app-get clean

# USER airflow

# File name: Dockerfile

FROM apache/airflow:latest 

USER root
RUN apt-get update --yes \
    && apt-get install --yes --no-install-recommends \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow
