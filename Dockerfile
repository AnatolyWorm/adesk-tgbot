FROM python:3.12.7-alpine

WORKDIR /opt/adesk-tgbot

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/opt/adesk-tgbot/src"

EXPOSE 80
CMD python src/main.py
