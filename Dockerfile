# Use the official Python base image
FROM python:3.10.11-slim

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app
    
# exposed port
EXPOSE 5800
# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

# Start the application
CMD ["service/service.py"]