FROM python:3.7.3-alpine3.9

LABEL maintainer="justin.payne@fda.hhs.gov"

WORKDIR /tmp

ADD requirements_dev.txt /tmp/
RUN pip install -r /tmp/requirements_dev.txt

WORKDIR /usr/src
ADD virfac/ /usr/src/

RUN make install \
  & make test