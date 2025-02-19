FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-update
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN mkdir configs out logs runs
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY . /app

CMD ["python3","app.py","--env","local"]