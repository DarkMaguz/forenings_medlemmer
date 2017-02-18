# Base the image off of python.
FROM python:latest

# Force stdin, stdout and stderr to be totally unbuffered.
ENV PYTHONUNBUFFERED 1

# Make the base directory for our app.
RUN mkdir /usr/app
WORKDIR /usr/app

# Copy python requirements file.
ADD requirements.txt /usr/app/
# Install from the requirements file.
RUN pip install -r requirements.txt

# Open port.
EXPOSE 8000

# Set the default command to be executed.
CMD ["/usr/app/docker-run.sh"]
