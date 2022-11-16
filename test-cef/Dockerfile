FROM ubuntu:20.04

USER root
RUN apt update -y

# timezone setting
ENV TZ=Asia/Tokyo
RUN apt install -y tzdata

RUN apt install -y git vim pip sudo

# cefore
RUN apt install libssl-dev
RUN git clone https://github.com/cefore/cefore.git
RUN cd cefore/ && \
  ./configure && \
  make && \
  sudo make install && \
  sudo ldconfig

# cefpyco
RUN apt install -y cmake python3-pip
RUN pip install setuptools click numpy
RUN git clone https://github.com/cefore/cefpyco.git
RUN cd cefpyco/ && \
  cmake . && \
  sudo make install
