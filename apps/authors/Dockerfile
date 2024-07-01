FROM python:3.12

RUN pip install 'strawberry-graphql[debug-server]' fastapi uvicorn

ADD . /src

WORKDIR /src
