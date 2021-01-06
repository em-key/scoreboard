# Dockerfile

# FROM directive instructing base image to build upon
FROM python:alpine

# # Update repository data and install nginx
RUN apk update && apk add --no-cache --virtual .build-deps gcc libffi-dev python3-dev musl-dev openssl-dev
RUN apk --no-cache add nginx bash

# COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# # Create folders for the webserver
RUN mkdir -p /opt/app/scoreboard

# # Copy dependincy files and install requirements.txt
COPY . /opt/app/scoreboard/
WORKDIR /opt/app/scoreboard/
RUN pip install -r requirements.txt

# Remove not required build packages
RUN apk del .build-deps

# # Expose Ports / start server
EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["./build_and_run/start-server.sh"]
