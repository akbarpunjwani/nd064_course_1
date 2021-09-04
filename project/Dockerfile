# --------
# -------- DOCKER FILE
# --------
# Step2A: Use a Python base image in version 2.7
# Base Image
FROM python:2.7
# --------
# Step2B: Expose the application port 3111
# make a container port available for exposure to host
EXPOSE 3111
# --------
# key/value label for image maintainer
LABEL maintainer="Akbar Punjwani"
# --------
# copy app files from the host to the container filesystem
COPY . /app
# --------
# define the working directory within the container
WORKDIR /app
# --------
# Step2C: Install packages defined in the requirements.txt file
# run commands within the container
#   invoke a pip command to install dependencies 
#   defined in the requirements.txt file. 
RUN pip install -r requirements.txt
# --------
# command to run at container start
#   the `init_db.py` to initialize db
#   the `app.py` to run application
# STEP2D:Ensure that the database is initialized with the 
#        pre-defined posts in the init_db.py file
CMD [ "python", "init_db.py" ]
# STEP2E:The application should execute at the container start
CMD [ "python", "app.py" ]
# --------
# -------- BUILD DOCKER IMAGE
# --------
# # STEP2F: Reference the defined Dockerfile
# # STEP2G: Tag the image as techtrends
# # STEP2H: Make sure you specify the location of the Dockerfile
# docker build -t techtrends -f ../Dockerfile .
# --------
# -------- RUN AND TEST LOCALLY
# --------
# # STEP2I: Using the detached mode (-d)
# # STEP2J: Expose the application port on port 7111 of host
# docker run -d -p 7111:3111 techtrends