FROM python:3.7

COPY . app

RUN cd app && pip install .

EXPOSE 8080
ENTRYPOINT [ "webhook-relay" ]
CMD [] 
