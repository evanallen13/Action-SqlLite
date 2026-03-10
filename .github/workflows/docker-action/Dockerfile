FROM python:3.12-slim

COPY entrypoint.py /entrypoint.py
COPY post.py /post.py
COPY requirements.txt /requirements.txt

RUN ls
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN chmod +x /entrypoint.py /post.py
