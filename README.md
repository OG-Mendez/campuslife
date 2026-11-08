# CampusLife

Student lodging platform: browse lodges, rate and review them, and use a points wallet to unlock room details. Agents manage rooms and earnings.

**Stack:** Django 5 + Django REST Framework, React (Vite), PostgreSQL 16, nginx, Docker Compose.

## Run it (clean clone)

Requires Docker with Compose v2. No API keys or internet access are needed to run the app.

```
git clone https://github.com/OG-Mendez/campuslife.git
cd campuslife
cp env.example .env
```

Open `.env` and set `SECRET_KEY` to any long random string (avoid `$` characters, since Compose treats them as variable references). Leave everything else blank.

```
docker compose up -d --build
docker compose exec web python manage.py seed_demo_data
```

The first build takes roughly 10 minutes (pip and npm installs). Later starts take seconds.

| Service  | URL                    |
|----------|------------------------|
| Frontend | http://localhost:3000  |
| API      | http://localhost:8000/api/ |
| Postgres | localhost:5432         |

## Demo logins

| Role    | Username       | Password       |
|---------|----------------|----------------|
| Student | `demo_student` | `DemoPass123!` |
| Agent   | `demo_agent`   | `DemoPass123!` |

The seed command is idempotent and deterministic (fixed data, fixed dates), so it is safe to re-run.

## Tests

With the stack running:

```
docker compose exec web coverage run manage.py test campuslife.tests
docker compose exec web coverage report -m
```

Covers model constraints, the payment and notification service layer (in offline mock mode), and the wallet flow: `fund_account`, `payment_callback` (including idempotency on duplicate callbacks) and `payment`.

## Offline behaviour and external services

Third-party integrations are isolated behind single classes and fall back to local behaviour when no credentials are set:

- **Payments (Paystack):** `campuslife_services/payments.py` (`PaystackService`). With no `PAYSTACK_SECRET_KEY` it returns deterministic mock responses.
- **Email:** `campuslife_services/notifications.py` (`NotificationService`). With no SMTP password it logs instead of sending; admin recipients come from `ADMIN_NOTIFICATION_EMAILS`.
- **Media storage:** `djangoProject2/settings.py` uses S3 only when AWS credentials are set; otherwise files are stored on a Docker volume and served at `/media/`.
- **Error tracking (Honeybadger):** optional, only active when `HONEYBADGER_API_KEY` is set.

The browser talks to a single origin: nginx serves the React build and proxies `/api/`, `/admin/`, `/media/` and `/static/` to Django.

## Layout

```
campuslife/            Django app (models, views, serializers, tests, seed command)
campuslife_services/   Isolated third-party integrations
djangoProject2/        Django project settings and URLs
client/                React (Vite) frontend, Dockerfile and nginx.conf
docker-compose.yml     db + web + frontend
entrypoint.sh          Waits for DB, migrates, collects static files
```

## Optional: restoring a Postgres dump

If you place a custom-format `pg_dump -Fc` file at `dbdump/backup.dump`, it is restored automatically into an empty database on first start. The folder is gitignored and not needed for review.
