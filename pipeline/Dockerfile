
FROM python:3.9

#postgres:15.1

#RUN apt-get update -y
#RUN apt-get install -y python \ 
#                          python3-pip 


WORKDIR /app 

# copies all contents currently in the directory to the container
COPY . /app

# install dependencies
RUN pip install -r requirements.txt

# run the sql script to create the database
ENTRYPOINT python3 /app/main.py
# This means: run the following command with bash (bahs located in bin)
#CMD ["/bin/bash", "-c", "sleep 10 && python3 /app/main.py"]





