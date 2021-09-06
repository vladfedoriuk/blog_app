# The first instruction is what image we want to base our container on
FROM python:3.8.2

RUN adduser --disabled-password --gecos '' blog

# The environment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# development
ENV DEBUG 1

# create root directory for our project in the container
RUN mkdir /code

# Copy the current directory contents into the container at /code
COPY . /code
RUN chown -R blog /code

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown blog /entrypoint.sh

USER blog
# Set the working directory to /code
WORKDIR /code

# Install any needed packages specified in requirements.txt
RUN pip install -r ./requirements/requirements.txt
ENTRYPOINT ["/entrypoint.sh"]