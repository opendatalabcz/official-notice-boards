FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

#RUN apt update
#RUN apt install tesseract-ocr -y

COPY . .

RUN pip install -e .
CMD [ "flask", "run" ]
