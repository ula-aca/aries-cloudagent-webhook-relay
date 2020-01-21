FROM python:3.7

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./webhook-relay.py .

EXPOSE 8080

ENTRYPOINT ["python", "-u", "./webhook-relay.py"]