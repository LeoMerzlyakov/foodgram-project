FROM python:3.8.5
LABEL author=leomerzlyakov@gmail.com project=footgram_project version=v1
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py load_ingredients
RUN python manage.py create_tags
CMD python manage.py runserver