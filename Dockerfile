FROM python:3
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow
RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-dev
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/ 
RUN useradd -p ceramicpassword ceramic
USER ceramic

