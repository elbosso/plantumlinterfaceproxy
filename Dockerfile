############################################################
# Dockerfile to build Flask App
# Based on
############################################################

# Set the base image
FROM ubuntu:latest

# File Author / Maintainer
MAINTAINER Jürgen Key

ENV DEBIAN_FRONTEND noninteractive    # export DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 \
    build-essential \
    python3 \
    python3-dev\
    python3-pip \
    joe \
    texlive texlive-lang-german texlive-latex-extra \
    graphicsmagick-imagemagick-compat \
    plantuml \
    gnuplot \
    firefox \
    locales locales-all \
 && locale-gen de_DE.UTF-8 \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

# Copy over and install the requirements
COPY ./app/requirements.txt /var/www/apache-flask/app/requirements.txt
RUN pip3 install -r /var/www/apache-flask/app/requirements.txt

# Copy over the apache configuration file and enable the site
COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf
RUN a2ensite apache-flask
RUN a2enmod headers

COPY ./geckodriver /var/www/apache-flask/

RUN chmod -R 777 /var/www

# Copy over the wsgi file
COPY ./apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi

COPY ./run.py /var/www/apache-flask/run.py
COPY ./app /var/www/apache-flask/app/
COPY ./app/static/index.html /var/www/
COPY ./formula.tex /var/www/apache-flask/

ENV LC_ALL de_DE.UTF-8

RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf

EXPOSE 80

WORKDIR /var/www/apache-flask

# CMD ["/bin/bash"]
CMD  /usr/sbin/apache2ctl -D FOREGROUND
# The commands below get apache running but there are issues accessing it online
# The port is only available if you go to another port first
# ENTRYPOINT ["/sbin/init"]
# CMD ["/usr/sbin/apache2ctl"]
