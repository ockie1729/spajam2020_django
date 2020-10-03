FROM python:3.8.5-buster

WORKDIR /opt/spajam
copy . .
RUN pip install -r requirements.txt
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:80
