FROM tiangolo/uvicorn-gunicorn:python3.8

WORKDIR /gbc_fastapi

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /gbc_fastapi/requirements.txt

RUN  pip --default-timeout=100  install  --no-cache-dir -r /gbc_fastapi/requirements.txt && \
     pip install flower && \
     rm -rf /root/.cache/pip

COPY . /gbc_fastapi

RUN chmod +x ./wait-for-it.sh

EXPOSE 80

CMD ["./wait-for-it.sh", "postgres:5432", "--", "uvicorn", "main:api", "--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive", "120"]



