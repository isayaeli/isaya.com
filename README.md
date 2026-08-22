# Isaya portfolio

Django portfolio site with a database-backed contact form.

## Run with Docker Compose

```sh
docker compose up --build
```

Open http://localhost:8000. Contact submissions are stored in the `sqlite_data` volume. The default email backend prints messages to the web container log; copy `.env.example` to `.env` and configure SMTP variables for delivery.

## Run the development environment

The development Compose file enables Django debug pages, mounts the source code, and runs Django's development server:

```sh
docker compose -f docker-compose.dev.yml up --build
```

Open http://localhost:8000 and submit the form. View the full traceback and request logs with:

```sh
docker compose -f docker-compose.dev.yml logs -f web
```

Stop it with `Ctrl+C`, or run `docker compose -f docker-compose.dev.yml down` in another terminal.

## Run locally

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
