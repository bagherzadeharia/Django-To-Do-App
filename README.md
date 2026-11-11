# Django To-Do App

A Django task manager with a server-rendered web interface and a Django REST Framework API. It includes custom email-based accounts, per-user tasks, email verification and password recovery, a weather endpoint, and background task processing.

## Features

- Sign up and sign in with an email address; verify accounts and recover passwords by email.
- Create, edit, complete, reopen, and delete tasks. Tasks are associated with their owner.
- Use the REST API with token or JWT authentication.
- Retrieve current weather for the city inferred from Django's configured time zone (OpenWeather geocoding and Open-Meteo forecast services).
- Cache API responses with Redis.
- Run scheduled Celery jobs to delete completed tasks.
- Browse the API schema with Swagger UI or ReDoc.
- Use the Persian, right-to-left web interface.

## Requirements

- Python 3.13 (the Docker image uses Python 3.13).
- Redis, required by the configured cache and Celery broker.
- PostgreSQL when `DEBUG=False`; local development uses SQLite when `DEBUG=True`.
- SMTP settings for sending verification and password reset emails. The Compose development setup includes smtp4dev.
- An OpenWeather API key for the weather endpoint.

Docker and Docker Compose are optional for running the Django web app locally, but simplify running Redis and smtp4dev.

## Run locally

Run commands from the repository root unless a step says otherwise.

1. Create and activate a virtual environment, then install dependencies:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a root `.env` file. You can copy `.env.sample` as a starting point, then set values for your environment:

   ```env
   DEBUG=True
   SECRET_KEY='your-secret-key-here'
   
   ALLOWED_HOSTS=*
   
   # Dev
   EMAIL_USE_TLS=False
   EMAIL_HOST='smtp4dev'
   EMAIL_HOST_USER='your-host-username'
   EMAIL_HOST_PASSWORD='your-host-password'
   EMAIL_PORT=25
   
   # Prod
   EMAIL_USE_TLS=True
   EMAIL_HOST='smtp.gmail.com'
   EMAIL_HOST_USER='your.email.address@gmail.com'
   EMAIL_HOST_PASSWORD='your smtp host pass'
   EMAIL_PORT=587
   
   POSTGRES_DB="something"
   POSTGRES_USER="something"
   POSTGRES_PASSWORD="something-something-something-dark-side"
   POSTGRES_HOST="not-something"
   
   CELERY_BROKER_URL='redis://redis-to-do-app:6379/0'
   ```

   `DEBUG=True` selects SQLite. Redis must be reachable at the configured cache location (`redis-to-do-app:6379`) or that cache location must be adjusted for your local Redis host. For email testing, smtp4dev's SMTP port is `25` in Compose; its web inbox is at <http://127.0.0.1:5000/>. `EMAIL_HOST` must match the SMTP service hostname reachable from Django.

3. Start Redis (and optionally smtp4dev), then migrate and run Django from `core/`:

   ```bash
   cd core
   python manage.py migrate
   python manage.py runserver
   ```

4. Visit <http://127.0.0.1:8000/>. Create an administrator if needed:

   ```bash
   python manage.py createsuperuser
   ```

   The admin site is at <http://127.0.0.1:8000/admin/>.

## Run with Docker Compose

The default Compose file starts the Django development server, Redis, smtp4dev, and Celery worker and beat services. Configure the root `.env` first. The Compose service names are already used for Redis and smtp4dev, so set `EMAIL_HOST=smtp4dev` and use the SMTP port exposed by the container (`25`).

```bash
docker compose up --build
```

In another terminal, run migrations:

```bash
docker compose exec to-do-app-backend python manage.py migrate
```

Open the app at <http://127.0.0.1:8000/> and the smtp4dev inbox at <http://127.0.0.1:5000/>. Stop the services with `docker compose down`.

The repository also contains `docker-compose-stage.yml`, which starts Gunicorn behind Nginx and a PostgreSQL service. Django uses PostgreSQL whenever `DEBUG=False`, so configure `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_HOST` in `.env` to match the database service before using that file. `docker-compose-prod.yml` is currently empty.

## Web routes

| Route | Description |
| --- | --- |
| `/` | Website home page |
| `/accounts/signup/` | Create an account |
| `/accounts/login/` | Sign in |
| `/accounts/logout/` | Sign out |
| `/todo/` | Task list |
| `/admin/` | Django administration |

## API routes

All API endpoints are under `/api/v1/` within the relevant app prefix.

| Route | Description |
| --- | --- |
| `/accounts/api/v1/registration/` | Register an account |
| `/accounts/api/v1/token/login/` | Obtain a DRF token |
| `/accounts/api/v1/jwt/create/` | Obtain a JWT token pair |
| `/accounts/api/v1/jwt/refresh/` | Refresh a JWT access token |
| `/accounts/api/v1/jwt/verify/` | Verify a JWT |
| `/accounts/api/v1/change-password/` | Change the authenticated user's password |
| `/accounts/api/v1/forget-password/` | Start password recovery |
| `/accounts/api/v1/verification/resend/` | Resend account verification email |
| `/todo/api/v1/tasks/` | List or create the authenticated user's tasks |
| `/todo/api/v1/tasks/{id}/` | Retrieve, update, or delete a task |
| `/weather/api/v1/` | Get cached weather data for the configured location |
| `/swagger/` | Interactive Swagger API documentation |
| `/redoc/` | ReDoc API documentation |
| `/swagger/output.json` | OpenAPI schema JSON |

Authenticate protected API requests with `Authorization: Token <key>` or `Authorization: Bearer <access-token>`. Task list filtering supports `title` and `complete`; ordering supports `updated_date`.

## Project layout

```text
.
├── core/
│   ├── accounts/       # Custom user model, web views, and auth API
│   ├── todo/           # Task model, web views, API, and Celery task
│   ├── weather/        # Weather API integration
│   ├── website/        # Home page
│   ├── templates/      # Django HTML and email templates
│   ├── static/         # CSS, JavaScript, and bundled static assets
│   ├── core/           # Django settings, URLs, and Celery configuration
│   └── manage.py
├── docker-compose.yml
├── docker-compose-stage.yml
├── Dockerfile
└── requirements.txt
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).
