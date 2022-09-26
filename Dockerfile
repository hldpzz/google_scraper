FROM selenium/standalone-chrome

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update
RUN yes | apt install python3-pip
RUN yes | apt install python3
RUN yes | pip install --no-cache-dir -r requirements.txt

COPY . .
CMD [ "python3", "./scraper.py" ]
