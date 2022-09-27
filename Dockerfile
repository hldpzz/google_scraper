FROM ubuntu:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY snaprm.sh ./
RUN chmod +x snaprm.sh
RUN apt update
RUN yes | apt install software-properties-common
RUN apt update
RUN add-apt-repository ppa:mozillateam/ppa
RUN sh snaprm.sh
RUN yes | apt-get install firefox
RUN yes | apt install python3-pip
RUN yes | apt install python3
RUN yes | pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python3","./scraper.py"] 
