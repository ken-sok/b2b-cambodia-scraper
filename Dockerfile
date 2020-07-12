FROM python:3.8
LABEL maintainer="chhaikheang.sok@gmail.com"
WORKDIR /src/app
COPY . . 
RUN apt-get update && apt-get install -y \
	python-pip
RUN pip3 install -r requirements.txt
CMD [ "python", "./scraper-b2b-docker.py" ]
