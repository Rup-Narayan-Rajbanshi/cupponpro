# first stage build
FROM python:3.8-slim AS base
MAINTAINER AAKARUI
# copy requirements
COPY requirements.txt ./
# install requirements
RUN pip install -r requirements.txt
# create app dir
WORKDIR /app
# copy everything to app dir
COPY . /app

# second stage build
FROM python:3.8-slim AS release
# needed to able run make command
RUN apt-get update && apt-get -qy install make libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info &&  rm -rf /var/lib/apt/lists/*
# needed for language translation support
RUN apt-get update && apt-get install -y gettext
# set work dir
WORKDIR /app
# copy everything from base
COPY --from=base /app/requirements.txt ./
COPY --from=base /root/.cache /root/.cache
# install requirements
RUN pip install -r requirements.txt
# copy again
COPY --from=base /app ./
