# Public website

Independent public information, publishing and enquiry website. Internal package names are functional so a change of company or product name does not require a repository restructure.

## Stack

- Python 3.13+ and Django 5.2 LTS
- Wagtail 7.4 LTS for controlled editorial publishing
- PostgreSQL in production; SQLite for local development
- Server-rendered templates, custom CSS and small vanilla JavaScript modules
- Gunicorn and WhiteNoise on Render

No code or database access is shared with the private institutional portal. The portal is linked through the configurable `PORTAL_URL` only.

## Local setup

```bash
uv venv --python 3.14 .venv
UV_CACHE_DIR=/tmp/public-website-uv-cache uv pip install --python .venv/bin/python --only-binary :all: -r requirements-dev.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_site
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

The editor is at `/site-admin/`. The initial content command is idempotent and will not overwrite existing editorial pages.

## Configuration

Required production values are `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `PUBLIC_SITE_URL`, `PORTAL_URL`, `SITE_NAME` and contact/email variables shown in `render.yaml`.

Brand names, colours, legal name, public contacts and the portal link are managed in Wagtail Site Settings or environment configuration. Do not introduce the current brand name into folder, package, service or database identifiers.

## Verification

```bash
.venv/bin/ruff check .
.venv/bin/pytest
.venv/bin/python manage.py makemigrations --check --dry-run
DJANGO_SETTINGS_MODULE=config.settings.production SECRET_KEY=test DATABASE_URL=sqlite:///production-check.sqlite3 ALLOWED_HOSTS=example.com CSRF_TRUSTED_ORIGINS=https://example.com PUBLIC_SITE_URL=https://example.com .venv/bin/python manage.py check --deploy
```

