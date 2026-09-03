# Django To-Do App

A small Django task manager with email-based authentication, as an exercise. Each signed-in user can create tasks, mark them complete or incomplete, edit them, and delete them.

## Features

- Email and password login
- Per-user task lists
- Create, edit, complete, reopen, and delete tasks
- SQLite database for local development
- Responsive Persian (RTL) interface
- Docker Compose development environment

## Tech stack

- Python 3.13
- Django 5.2
- SQLite
- Docker and Docker Compose (optional)

## Quick start

### Run locally

1. Clone the repository and enter the project directory.

   ```bash
   git clone <repository-url>
   cd Django-To-Do-App
   ```

2. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the repository root.

   ```env
   DEBUG=True
   SECRET_KEY=replace-with-a-long-random-secret
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Apply migrations and start the development server.

   ```bash
   cd core
   python manage.py migrate
   python manage.py runserver
   ```

6. Open <http://127.0.0.1:8000/> and sign in. To create an admin user, run:

   ```bash
   python manage.py createsuperuser
   ```

   You can then use the Django admin at <http://127.0.0.1:8000/admin/>.

### Run with Docker Compose

1. Create the `.env` file shown above.
2. Start the development container:

   ```bash
   docker compose up --build
   ```

3. Apply migrations in the running container:

   ```bash
   docker compose exec to-do-app-backend python manage.py migrate
   ```

The application is available at <http://127.0.0.1:8000/>. Stop it with `docker compose down`.

## Project structure

```text
core/
├── accounts/       # Custom email-based user model and login flow
├── todo/           # Task model, forms, views, and URLs
├── templates/      # Login and task-manager templates
├── core/           # Django settings and project URL configuration
└── manage.py
```

## Main routes

| Route | Description |
| --- | --- |
| `/` | Authenticated task list |
| `/accounts/login` | Sign in |
| `/accounts/logout` | Sign out |
| `/admin/` | Django administration |

## License

This project is licensed under the [Apache License 2.0](LICENSE).
