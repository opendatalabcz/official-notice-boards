FROM python:3.10

# TODO change
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]