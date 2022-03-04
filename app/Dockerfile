# syntax=docker/dockerfile:1

################################################
# BASE
################################################
FROM python:3.9 AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /movieguessr
COPY requirements.txt /movieguessr/
RUN pip3 install -r requirements.txt

# Add docker-compose-wait tool -------------------
# This is needed for Django to wait for the PostgreSQL database to be running bofore continuing.
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait

# Set the execute permissions.
RUN chmod +x /wait

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME


################################################
# PRODUCTION 
################################################
FROM base as prod

# create the app user
RUN addgroup --system app 
RUN adduser app --ingroup app

# create the appropriate directories
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app