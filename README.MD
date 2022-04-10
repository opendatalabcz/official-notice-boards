# How to run:
## A) using docker-compose
1. Make sure you have docker installed. Download link: https://www.docker.com/products/docker-desktop/
2. To start the website run `docker-compose up -d`

[//]: # (3. To start data extraction run `flask import_all` # TODO will be decided based on data approach)

## B) locally
1.     python3.10 -m venv venv
2.     source venv/bin/activate
3.     pip install -e .
4. change database URI in the .env file (Postgresql required)
5. to run website run `flask run`
6. to import all data run `flask import_all`