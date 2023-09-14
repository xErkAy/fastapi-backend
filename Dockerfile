FROM python:3.11

WORKDIR /backend

RUN apt-get update && \
    apt-get install -y wget lsb-release && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    (wget --no-check-certificate --quiet -O - https://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -)

RUN pip install  --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir fastapi uvicorn[standard]

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /backend .

CMD [ "/bin/bash", "entrypoint.sh" ]