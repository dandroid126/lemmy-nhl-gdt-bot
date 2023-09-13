FROM docker.io/python:3.11-alpine3.18

WORKDIR /app
RUN adduser -D python
RUN install -d -m 700 -o python -g python out
COPY src src
COPY requirements.txt requirements.txt

USER python
ENV PYTHONPATH='/app'
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "src/main.py" ]

# Uncomment the line below to hold open a container failing to start for debugging purposes
# CMD [ "sleep", "infinity" ]
