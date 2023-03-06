FROM python:3.9-alpine3.13
# ensures that the desired python version is being used

LABEL maintainer="dev-Jonnathan"
# it is the name of who is being maintaining the app

ENV PYTHONUNBUFFERED 1
# recommended when python is being used in a docker container
# it tells python that the output will not be buffered, it will be printed directly in the terminal

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# copies the file "requirements.txt" from the local machine into the docker image
COPY ./app /app
# copies the "app" directory from the local machine to the container
WORKDIR /app
# sets the default directory that the commands will be running from
EXPOSE 8000
# connects to the django development server

ARG DEV=false
RUN python -m venv /py && \ 
    # creates a new virtual environment
    /py/bin/pip install --upgrade pip && \ 
    # upgrades pip for the virtual environment that has been created
    apk add --update --no-cache postgresql-client && \
    # installs the package postgresql-client (dependency package)
    apk add --update --no-cache --virtual .tmp-build-deps \
    # sets a virtual dependency package at .tmp-build-deps to be used to remove the dependencies unused packages
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \ 
    # installs the list requirements file
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    # fi && (it is the default way to end an if quote)
    rm -rf /tmp && \ 
    apk del .tmp-build-deps && \
    # removes the tmp directory (to eliminate extra dependencies on the image once has been created)
    adduser \ 
        --disabled-password \
        --no-create-home \
        django-user
    # adds a new user inside the just created image

ENV PATH="/py/bin:$PATH"
# updates the environment variable inside the image

USER django-user
# specifies the user that it is being used 
