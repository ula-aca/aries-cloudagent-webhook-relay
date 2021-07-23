FROM python:3.7

COPY . app

RUN cd app && pip install .

EXPOSE 8022
ENTRYPOINT [ "webhook-relay" ]
CMD [] 
