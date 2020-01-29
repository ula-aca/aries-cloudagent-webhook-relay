FROM python:3.7

COPY . app

RUN PYTHONPATH=${PYTHONPATH}:/usr/local/lib/python3.6/site-packages
RUN cd app && pip install .

EXPOSE 8080
ENTRYPOINT [ "webhook-relay" ]
CMD [] 