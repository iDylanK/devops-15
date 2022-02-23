# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /movieguessr
COPY requirements.txt /movieguessr/
RUN pip3 install -r requirements.txt
COPY . /movieguessr/

# RUN python3 manage.py migrate

# Add docker-compose-wait tool -------------------
# This is needed for Django to wait for the PostgreSQL database to be running bofore continuing.
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait

# Done inside the docker-compose.yml
# RUN chmod +x /wait

# CMD ["python3 manage.py migrate"]