FROM python:3.9
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "4", "app.app:app"]
