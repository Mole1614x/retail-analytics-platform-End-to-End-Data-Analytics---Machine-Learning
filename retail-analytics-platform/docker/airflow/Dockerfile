
FROM apache/airflow:2.10.5-python3.10

USER root

RUN apt-get update && \
    apt-get install -y docker.io default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"


USER airflow

RUN pip install --no-cache-dir pandas matplotlib scikit-learn joblib pyspark==3.5.0
