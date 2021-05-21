FROM python:3.8.5
LABEL author=leomerzlyakov@gmail.com project=footgram_project version=v2_Postgres
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic