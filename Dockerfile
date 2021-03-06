FROM python:3.8.5-slim

WORKDIR /usr/src/app

LABEL maintainer="Milo van der Linden - https://www.tiltshiftapps.nl"

ENV DATABASE_URL "postgresql://postgres:postgres@127.0.0.1:5432/postgres"
ENV BACKEND_CORS_ORIGINS_CSV "http://localhost,http://localhost:4200,http://localhost:3000"
ENV AMSTERDAM_PRIMARY_SCHOOLS "https://schoolwijzer.amsterdam.nl/nl/api/v1/lijst/po"
ENV AMSTERDAM_HIGH_SCHOOLS "https://schoolwijzer.amsterdam.nl/nl/api/v1/lijst/vo"
ENV AMSTERDAM_KINDERGARTEN "https://schoolwijzer.amsterdam.nl/nl/api/v1/lijst/opvang"
ENV AMSTERDAM_DAYCARE "https://schoolwijzer.amsterdam.nl/nl/api/v1/lijst/bso"
ENV USERS '{"demo": "test12345"}'

RUN apt-get update && apt-get install -y \
    gcc postgresql-client libpq-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
VOLUME ["/usr/src/app/data"]
CMD [ "./mini-crm.sh" ]
