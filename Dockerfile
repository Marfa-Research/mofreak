FROM ubuntu:16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        ffmpeg \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        python-dev \
        python-numpy \
        python-pip \
        python-setuptools \
        python-scipy \
        python-opencv \
        libjpeg-dev \
        libtiff-dev \
        libjasper-dev \
        libpng-dev \
        libgtk2.0-dev && \
    rm -rf /var/lib/apt/lists/*

ENV OPENCV_VERSION 3.2.0

RUN git clone -b OPENCV_VERSION https://github.com/opencv/opencv_contrib /usr/local/opencv_contrib && \
    git clone -b OPENCV_VERSION https://github.com/opencv/opencv /usr/local/opencv && \
    mkdir /usr/local/opencv/build

WORKDIR /usr/local/opencv/build

RUN cmake -D OPENCV_EXTRA_MODULES_PATH=/usr/local/opencv_contrib/modules/ .. && \
    make -j"$(nproc)" && make install && ldconfig

WORKDIR /srv
