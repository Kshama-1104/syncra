# Syncra Step-by-Step Guide

## 1. Project Architecture

Syncra separates HTTP APIs and WebSockets because they scale differently. DRF runs behind Gunicorn for regular REST traffic. Channels runs behind Daphne for long-lived WebSocket connections. Redis is the channel layer that lets multiple Daphne workers broadcast events to the correct rooms. PostgreSQL stores source-of-truth relational data. Celery handles slow work such as email, notification fanout, media processing, and scheduled cleanup.

## 2. Folder Structure

The monorepo has `backend`, `frontend`, `infra`, `docs`, and `.github/workflows`. This keeps deployment, code, and documentation in one resume-ready repository while preserving clean backend/frontend boundaries.

## 3. Backend Setup

```bash
cd syncra/backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On Windows PowerShell, activate with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 4. PostgreSQL

Local Docker Compose starts PostgreSQL automatically. In production, prefer a managed Postgres instance or a dedicated volume with daily backups. Use connection pooling when traffic grows.

## 5. Redis

Redis powers four concerns: Channels fanout, Celery broker, cache, and short-lived presence state. For production scale, use a managed Redis service or a Redis cluster with eviction policies configured intentionally.

## 6. Channels and ASGI

`config/asgi.py` routes HTTP to Django and WebSockets to `ChatConsumer`. `common/middleware/jwt_ws.py` authenticates WebSocket requests with the `?token=` query parameter. For browser security, use short-lived JWTs and reconnect with a fresh access token after refresh.

## 7. Authentication

The scaffold includes register/login and JWT refresh. Next production steps are:

- email verification token model or signed URL flow;
- password reset with signed expiring tokens;
- Google OAuth through `django-allauth` or direct Google ID token verification;
- refresh token rotation and blacklist app enabled before public launch.

## 8. Chat Flow

1. User logs in and receives JWT access/refresh tokens.
2. Frontend fetches `/api/v1/chats/`.
3. User opens a chat.
4. Frontend connects to `/ws/chats/<id>/?token=<access>`.
5. Consumer verifies membership.
6. Message events are persisted to PostgreSQL.
7. Redis channel layer broadcasts the event to every connection in the chat room.
8. Clients update UI immediately.

## 9. Query Optimization

Use `select_related` for single foreign keys and `prefetch_related` for memberships/messages. Keep message pagination cursor-based for very large chats. Avoid loading full message bodies in chat list endpoints once volume grows; use a denormalized `last_message_id` on `Chat`.

## 10. Security

Production security settings are already present: secure cookies, HSTS, HTTPS redirect, X-Frame-Options, CORS, CSRF trusted origins, JWT auth, serializer validation, ORM queries, and upload size validation. Add rate limits on auth and message endpoints before public launch.

## 11. Frontend Setup

```bash
cd syncra/frontend
npm install
cp .env.example .env
npm run dev
```

The frontend uses Axios interceptors for JWT refresh and a reconnecting WebSocket hook with exponential backoff.

## 12. Docker

```bash
cd syncra
docker compose up -d --build
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
```

## 13. VPS Deployment

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin nginx certbot python3-certbot-nginx git
sudo usermod -aG docker $USER
sudo mkdir -p /opt/syncra
sudo chown $USER:$USER /opt/syncra
git clone https://github.com/YOUR_USERNAME/syncra.git /opt/syncra
cd /opt/syncra
cp backend/.env.example backend/.env
nano backend/.env
docker compose up -d --build
docker compose exec backend python manage.py migrate --noinput
docker compose exec backend python manage.py createsuperuser
```

Point your DNS A record to the VPS IP, then run:

```bash
sudo certbot --nginx -d syncra.example.com
```

For the Compose Nginx container approach, mount certificates into `infra/ssl` or terminate TLS at host Nginx/load balancer and proxy to the Docker Nginx container.

## 14. CI/CD

CI installs backend/frontend dependencies, checks migrations, runs Django deployment checks, lints Python, runs tests, and builds the frontend. Deployment uses SSH to pull the latest branch and restart Docker Compose. Add repository secrets: `VPS_HOST`, `VPS_USER`, and `VPS_SSH_KEY`.

## 15. Common Mistakes

- WebSocket 401: access token expired or user is not a chat member.
- Messages duplicate: sending through both REST and WS at the same time.
- CORS failure: `FRONTEND_URL` does not match the exact browser origin.
- Static files missing: run `collectstatic` and confirm Nginx volume mount.
- Migrations missing: run `makemigrations` after model changes and commit migration files.
- Redis connection refused: check `REDIS_URL` differs between local and Docker.

## 16. Next Build Milestones

1. Add migrations and admin registration.
2. Complete email verification and password reset.
3. Add Google OAuth.
4. Add S3/Cloudinary storage backend.
5. Add message attachments table linked to `MediaAsset`.
6. Add cursor pagination for messages.
7. Add notification WebSocket consumer.
8. Add backend websocket tests with `WebsocketCommunicator`.
9. Add frontend tests with React Testing Library.
10. Add monitoring with Sentry and structured logs.
