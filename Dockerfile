FROM python:3.10.9

COPY API/ /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "./main.py"]
