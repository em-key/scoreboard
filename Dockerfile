# Dockerfile

##### INFO #####
#
# Before Build run python manage.py collectstatic
#
################

# FROM directive instructing base image to build upon
FROM python:alpine

# # Update repository data and install nginx
RUN apk update && apk add --no-cache --virtual .build-deps gcc libffi-dev python3-dev musl-dev openssl-dev
RUN apk --no-cache add nginx bash

# # Create folders for the webserver
RUN mkdir -p /opt/app/scoreboard

# # Copy dependincy files and install requirements.txt
COPY . /opt/app/scoreboard/
WORKDIR /opt/app/scoreboard/
RUN pip install -r requirements.txt

# Remove not required build packages
RUN apk del .build-deps

# Setup Nginx
COPY ./build_and_run/nginx.conf /etc/nginx/nginx.conf
COPY ./build_and_run/default.conf /etc/nginx/conf.d/default.conf

RUN chown -R nginx:nginx /opt/app && \
    # chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# change user
USER nginx

# # Expose Ports / start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["./build_and_run/start-server.sh"]
