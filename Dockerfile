FROM python:3.10.7-slim
# set work directory
WORKDIR /project
# copy project
COPY . /project
# install dependencies
COPY ./requirements.txt /project/requirements.txt
RUN pip install -r requirements.txt