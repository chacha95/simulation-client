FROM python:3.9.7
LABEL maintainer="chacha, ckwlsgur20@gmail.com"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates python3-dev git wget sudo
RUN ln -sv /usr/bin/python3 /usr/bin/python

# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser

RUN pip install bokeh
RUN pip install zarr

RUN git clone https://github.com/chacha95/${REPO_NAME}
WORKDIR /home/appuser/${REPO_NAME}