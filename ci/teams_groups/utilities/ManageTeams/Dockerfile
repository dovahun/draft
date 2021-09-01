FROM ubuntu:20.10

ARG fly_version="6.6.0"
ARG yq_version="3.4.0"

RUN apt-get update && apt-get install -y wget &&\
    wget https://github.com/concourse/concourse/releases/download/v"$fly_version"/fly-"$fly_version"-linux-amd64.tgz && \
    tar -xvf fly-"$fly_version"-linux-amd64.tgz && \
    mv fly /usr/bin && \
    rm -fr fly-"$fly_version"-linux-amd64.tgz && \
    chmod +x /usr/bin/fly  && \
    wget https://github.com/mikefarah/yq/releases/download/"$yq_version"/yq_linux_amd64 -O /usr/bin/yq && \
    chmod +x /usr/bin/yq

WORKDIR app

COPY . .
