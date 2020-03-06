# pull official base image
FROM python:3.8.1-alpine

# set work directory
WORKDIR /usr/src/quiz_me

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/quiz_me/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/quiz_me/