FROM ubuntu

RUN apt-get update

# install python
RUN apt-get -y install python2.7

# install curl
RUN apt-get -y install curl

# install python-tools
RUN apt-get -y install python-setuptools python-dev build-essential

# install redis module
RUN easy_install redis

# add python script
ADD urlFilter.py /usr/local/bin/urlFilter.py

# expose port
EXPOSE 8080

# Set default container command
ENTRYPOINT /usr/bin/python2.7 /usr/local/bin/urlFilter.py
