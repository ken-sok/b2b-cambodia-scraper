#!/bin/bash

#this builds all images needed to run container & runs it
docker-compose run --name b2b-scraper-con scraper 

# this stores the python script's container id
CONTAINER_ID=$(docker ps -aqf "name=^b2b-scraper-con$")

#this stores username

#copy excel from container to host
docker cp $CONTAINER_ID:/src/app/b2b-page-excel/ D:/

#get webdriver container ID
SELENIUM_CONTAINER_ID=$(docker ps -aqf "name=^click-next$")

#stop & remove containers
docker stop $SELENIUM_CONTAINER_ID
docker rm $SELENIUM_CONTAINER_ID
docker rm $CONTAINER_ID
