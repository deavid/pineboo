FROM ubuntu:19.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    python3-dev python3-pip python3-psycopg2 python3-mysqldb python3-pymysql python3-venv \
    xvfb libfontconfig1 && \
    rm -rf /var/lib/apt/lists/*

COPY pip-requirements.txt /

RUN pip3 install -r /pip-requirements.txt --prefer-binary --upgrade --no-cache-dir
