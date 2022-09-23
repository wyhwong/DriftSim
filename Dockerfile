FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt install -y python3 python3-pip -y
RUN pip3 install --upgrade pip
RUN pip install matplotlib numpy pycbc scipy bilby #lalsimulation
