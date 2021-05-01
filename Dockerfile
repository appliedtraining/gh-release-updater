FROM python:3.9-slim

COPY entrypoint.sh /entrypoint.sh
WORKDIR /app
COPY ./src .
RUN pip install pip-tools && pip-sync requirements.txt

ENTRYPOINT ["/entrypoint.sh"]
