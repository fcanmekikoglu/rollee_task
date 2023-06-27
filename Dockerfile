FROM python:3.11

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /rollee_task

COPY . /rollee_task

RUN pip install -r requirements.txt

EXPOSE 8000

CMD sh -c "sleep 5 && python3 manage.py makemigrations && python3 manage.py migrate && python manage.py runserver 0.0.0.0:8000 "
