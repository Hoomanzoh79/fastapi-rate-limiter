FROM hub.hamdocker.ir/python:3.13-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./src /code/src

# Configure pip and install requirements
RUN pip config set global.break-system-packages true \
    && pip config set global.index https://repo.hmirror.ir/python/simple\
    && pip config set global.index-url https://repo.hmirror.ir/python/simple\
    && pip install --no-cache-dir -r requirements.txt 

EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000"]