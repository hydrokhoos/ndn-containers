FROM ubuntu:20.04

USER root
RUN apt update -y

# timezone setting
ENV TZ=Asia/Tokyo
RUN apt install -y tzdata

RUN apt install -y git vim pip sudo

# proactive
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:named-data/ppa
RUN apt update -y
RUN apt install -y libpcap-dev libsystemd-dev pkg-config

# ndn-python
RUN pip install python-ndn
RUN git clone https://github.com/named-data/python-ndn.git

# ndn-cxx
RUN git clone https://github.com/named-data/ndn-cxx.git
RUN apt-get install -y build-essential libsqlite3-dev libboost-all-dev libssl-dev
RUN cd ndn-cxx && \
  ./waf configure && \
  ./waf && \
  ./waf install && \
  ldconfig

# NFD
RUN git clone --recursive https://github.com/named-data/NFD.git
ENV PKG_CONFIG_PATH /custom/lib/pkgconfig
RUN cd NFD && \
  ./waf configure && \
  ./waf && \
  ./waf install
RUN cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf

# PSync library
RUN git clone https://github.com/named-data/PSync.git
RUN cd PSync && \
  ./waf configure && \
  ./waf &&\
  ./waf install

# ndn-tools
RUN git clone https://github.com/named-data/ndn-tools.git
RUN cd ndn-tools && \
  ./waf configure && \
  ./waf && \
  ./waf install

# NLSR
RUN git clone https://github.com/named-data/NLSR.git
RUN cd NLSR && \
  ./waf configure && \
  ./waf && \
  ./waf install && \
  ldconfig
RUN mkdir /var/lib/nlsr

# COPY ./src/ /src

CMD ["/usr/sbin/init"]
