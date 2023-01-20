FROM python:alpine3.17

RUN pip3 install python-telegram-bot

WORKDIR /usr/app/src

COPY run.py ./

CMD [ "python", "./run.py"]
