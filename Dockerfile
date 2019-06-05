FROM alpine:latest

RUN apk add --no-cache python3-dev libffi-dev build-base zlib-dev py-pip jpeg-dev \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["run.py"]
