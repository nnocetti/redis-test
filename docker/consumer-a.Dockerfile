FROM python:3

# set the working directory in the container
WORKDIR /opt/src

# copy the dependencies file to the working directory
COPY ./src/requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "./consumer-a.py"]