# b2b-page-scraper
This image is used to scrape https://www.b2b-cambodia.com/ directory and return all company details into an excel file. 


###Documentation

I. First time use:

	1. Install docker toolbox on https://docs.docker.com/toolbox/toolbox_install_windows/ 
	*Important Note: DO NOT install Docker Windows as it is not tested

	2. Open Docker Quickstart terminal on your desktop, and go to folder of your files with the 'cd <directory>'
    command

	3. Type 'docker-compose build' into the Docker Quickstart terminal

	4. After successfully built container, you should see 'Successfully tagged b2b-scraper:latest' at last line

	5. Type './run-app.sh' into the Docker Quickstart terminal

    6. Input URL and local host address as requested
	
    7. When the app finishes, check D:/b2b-page-excel for your companies information 
    in a csv format

II. For reuse: 

	1. Open Docker Quickstart terminal on your desktop, and go to folder of your files with the 'cd <directory>'
    command

	2. Type './run-app.sh' into the Docker Quickstart terminal

    3. Input URL and local host address as requested

	4. When the app finishes, check D:/yellow-page-excel for your companies information 
    in an excel format

Note: 
-when using cd <directory>, if you copy windows directory, please use single quotes to
cover directory. For example, cd 'C:/Users/tom/desktop/b2b-docker'
-if you want to tinker with the code, please do a 'docker-compose down -v' before you rebuild a new docker image/container

Known issues:
-sometimes the b2b page crashes, you can retry a few times, it should work. 


