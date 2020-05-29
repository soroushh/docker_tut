FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN apk --no-cache add libffi-dev
RUN python3 -m pip install psycopg2


WORKDIR /user/src/app

COPY . .

EXPOSE 5000

ENV PSYCOPG_DEBUG=1


RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./app.py"]
