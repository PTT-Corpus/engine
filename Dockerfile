FROM python:3.6.6-alpine3.8

ENV ELASTICSEARCH_HOST 140.112.147.121
ENV ELASTICSEARCH_PORT 19200

EXPOSE 80

COPY ./api /app

WORKDIR /app
RUN pip3 install -r requirements/prod.txt
# RUN gunicorn -b 0.0.0.0:80 app:api
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:api"]
