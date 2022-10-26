FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip -y
RUN pip3 install --upgrade pip
RUN pip install jupyterthemes notebook matplotlib numpy pycbc scipy bilby #lalsimulation
RUN jt -t monokai
