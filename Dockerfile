# Base Image
FROM python:3.7-alpine

WORKDIR /usr/app

# Install some depenendencies
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

# Default command
CMD ["python", "app.py"]

EXPOSE 5000/tcp