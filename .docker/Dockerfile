FROM python:3.10.4-alpine

WORKDIR /app

RUN pip install pipenv==2022.4.8
COPY ./Pipfile ./
RUN python3.10 -m pipenv install

COPY ./application ./application
COPY ./domain ./domain
COPY ./infrastructure ./infrastructure
COPY ./app.py ./
COPY ./.configs ./.configs

ENTRYPOINT [ "sh", "-c", "pipenv run flask run --host=0.0.0.0" ]