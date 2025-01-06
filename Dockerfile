FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip  && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY . /app
COPY .env .env

RUN pip3 install -r requirements.txt


CMD ["python3", "main.py"]