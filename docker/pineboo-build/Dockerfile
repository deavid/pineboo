FROM ubuntu:19.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git libglib2.0-0 libfontconfig1 libgl1-mesa-glx \
    moreutils make \
    python3-pip python3-setuptools \
    python3-psycopg2 python3-mysqldb python3-pymysql python3-venv python3-cryptography \
    && \
    rm -rf /var/lib/apt/lists/*

COPY pip-requirements.txt /

RUN pip3 install -r /pip-requirements.txt --prefer-binary --upgrade --no-cache-dir
