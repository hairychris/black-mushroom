FROM alpine:edge

RUN apk update && \
  apk --update add py3-greenlet py3-psycopg2

ONBUILD RUN python3 -m ensurepip && \
  rm -r /usr/lib/python*/ensurepip

RUN pip3 install --upgrade pip setuptools && \
  rm -r /root/.cache

WORKDIR /var/nameko/
COPY ./src/services /var/nameko/services
COPY ./config.yml /var/nameko/config.yml

RUN pip3 install /var/nameko/services/base && \
  pip3 install /var/nameko/$SERVICE

EXPOSE 8000
CMD /usr/bin/nameko run black_mushroom.$SERVICE.services --config /var/nameko/config.yml;