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

## Deploy to GitHub Pages

`.github/workflows/pages.yml` builds a static copy of the site on every push to `main` and publishes it to https://isayaeli.github.io/isaya.com/. In that build the contact form posts to [Formspree](https://formspree.io) instead of Django.

One-time setup:

1. Create a Formspree form and copy its endpoint (`https://formspree.io/f/<id>`).
2. Save it as the repository variable `FORMSPREE_ENDPOINT` (Settings → Secrets and variables → Actions → Variables, or `gh variable set FORMSPREE_ENDPOINT`).
3. Set Settings → Pages → Source to **GitHub Actions**.

Build it locally with:

```sh
python manage.py build_site --base-url http://localhost:8001 --formspree https://formspree.io/f/test
python -m http.server 8001 -d dist
```
