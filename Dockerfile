# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim-buster

# Copy local code to the container image.
ENV APP_HOME /app
ENV PYTHONUNBUFFERED True
WORKDIR $APP_HOME

# Intall UNIX dependencies
RUN sed -i -e's/ main/ main contrib non-free/g' /etc/apt/sources.list \
&& apt-get -q update && apt-get install unrar git -y

# Install Python dependencies and Gunicorn
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN groupadd -r app && useradd -r -g app app

# Copy the rest of the codebase into the image
COPY --chown=app:app . ./
RUN chown -R app:app .
RUN chmod 755 .
USER app

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available in Cloud Run.
CMD exec gunicorn --bind :$PORT --log-level info --workers 1 --threads 8 --timeout 0 app:server
