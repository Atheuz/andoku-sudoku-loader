from myoung34/github-runner:latest

RUN ln /usr/bin/python3.7 /usr/bin/python \
 && apt-get update \
 && apt-get install -y --no-install-recommends python3-pip python3-setuptools build-essential \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
