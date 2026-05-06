# Free Deployment Path

Use this path when you need Syncra online without paying:

- Backend: Render Free Web Service
- Database: Neon Free PostgreSQL
- Redis: Upstash Free Redis
- Frontend: Vercel Hobby

Free limitations:

- Render free web services sleep after idle time.
- Free services are suitable for portfolio/demo use, not serious production traffic.
- File uploads on Render's free filesystem are temporary after restarts/redeploys. Use S3/Cloudinary later for permanent media.

## Backend Render Commands

Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Start command:

```bash
python manage.py migrate --noinput && daphne -b 0.0.0.0 -p $PORT config.asgi:application
```

## Required Backend Environment Variables

```env
DJANGO_SECRET_KEY=<generated-secret>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<your-render-backend-host>
FRONTEND_URL=<your-vercel-frontend-url>
DATABASE_URL=<neon-postgres-url>
REDIS_URL=<upstash-redis-url>
SECURE_SSL_REDIRECT=False
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=Syncra <noreply@syncra.app>
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

## Required Frontend Environment Variables

```env
VITE_API_URL=https://<your-render-backend-host>/api/v1
VITE_WS_URL=wss://<your-render-backend-host>/ws
```
