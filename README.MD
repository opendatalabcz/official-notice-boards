# How to run:
## Using docker-compose
1. Make sure you have docker installed. Download link: https://www.docker.com/products/docker-desktop/
2. To start the website run `docker-compose up -d`
3. Open container shell ` docker exec -it  official-notice-boards_db_1  bash`
4. To import all data run `flask import_all_data` inside the container shell (This will take multiple hours)
5. To import new data since the last import, run `flask import_new_data` inside the container shell

[//]: # (## B&#41; locally)

[//]: # (1.     python3.10 -m venv venv)

[//]: # (2.     source venv/bin/activate)

[//]: # (3.     pip install -e .)

[//]: # (4. change database URI in the .env file &#40;Postgresql required&#41;)

[//]: # (6. to import all data run `flask import_all_data`)

[//]: # (5. to run website run `flask run`)
