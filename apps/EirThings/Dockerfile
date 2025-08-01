# app/Dockerfile

FROM python:3.11-slim

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY . /app

EXPOSE 8501

ENTRYPOINT ["python3", "app.py"]