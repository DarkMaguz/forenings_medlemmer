# Base the image off of python.
FROM python:latest

# Force stdin, stdout and stderr to be totally unbuffered.
ENV PYTHONUNBUFFERED 1

# Make the base directory for our app.
RUN mkdir /usr/app
WORKDIR /usr/app

#ADD . /usr/app/
ADD requirements.txt /usr/app/
RUN pip install -r requirements.txt
#ADD . /usr/app/

#RUN python manage.py migrate
#RUN python manage.py loaddata fixtures/templates.json
#RUN python manage.py loaddata fixtures/unions.json
#RUN python manage.py loaddata fixtures/departments.json

# Open port
EXPOSE 8000

CMD ["/usr/app/docker-run.sh"]
