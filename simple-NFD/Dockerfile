FROM ubuntu:20.04

RUN apt update -y
RUN apt install software-properties-common python3 -y
RUN add-apt-repository ppa:named-data/ppa
RUN apt update -y
RUN apt install nfd -y

RUN apt install pip git -y
RUN pip install python-ndn
RUN git clone https://github.com/named-data/python-ndn

ENTRYPOINT ["/usr/sbin/init"]
