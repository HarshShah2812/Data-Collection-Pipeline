FROM python:3.10

# update the system and install Firefox
RUN apt-get update
RUN apt -y upgrade
RUN apt-get install -y firefox-esr

# get the latest release of geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux32.tar.gz \
    # extract the geckodriver
    && tar -xvzf geckodriver* \
    # add executable permissions to the driver
    && chmod +x geckodriver \
    # move geckodriver to the system path
    && mv geckodriver /usr/local/bin

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "DCP.py"]

