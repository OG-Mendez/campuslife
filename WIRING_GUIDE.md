# Wiring it all together

## 1. Drop in the new package
Copy `campuslife_services/` (this folder) into your repo root, next to the
`campuslife` app — or inside it as `campuslife/services/`, either works, just
update the import paths below to match.

## 2. settings.py changes

Add `HONEYBADGER_API_KEY` and `ADMIN_NOTIFICATION_EMAILS` to your `.env.example`.

Replace the hardcoded Honeybadger block:
```python
HONEYBADGER = {
  'API_KEY': 'hbp_ilYE2NA8C0FwqK2nl5T10fADYdaLKg4ErzL4'
}
```
with:
```python
HONEYBADGER = {"API_KEY": os.getenv("HONEYBADGER_API_KEY", "")}
```

Replace the hardcoded Cloudinary block:
```python
cloudinary.config(
    cloud_name='dem4ececb',
    api_key='361993149326335',
    api_secret=os.getenv("CLOUD_API_SECRET")
)
```
with:
```python
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET"),
)
```

Replace the media/storage block:
```python
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "campuslife1"
AWS_S3_CUSTOM_DOMAIN = "d2vsftgl2k06m2.cloudfront.net"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
MEDIA_ROOT = "media/"
```
with:
```python
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "campuslife1")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", "")

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    # Real S3 bucket configured — use it.
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
else:
    # No S3 creds (local/offline/review) — serve media from disk instead.
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
```

Add near the email settings, replacing the fixed SMTP backend:
```python
if os.getenv("EMAIL_HOST_PASSWORD"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    # No SMTP password configured — print emails to the console/logs
    # instead of failing. Fine for local dev and offline review.
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

## 3. urls.py — serve local media when using FileSystemStorage
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...your existing patterns...
]

if settings.DEBUG and settings.DEFAULT_FILE_STORAGE.endswith("FileSystemStorage"):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 4. views.py — route through the service classes

Replace the direct Paystack import:
```python
from paystackapi.transaction import Transaction
```
with:
```python
from campuslife_services.payments import PaystackService
```

In `fund_account`, replace:
```python
transaction = Transaction.initialize(
    key=os.getenv('PAYSTACK_SECRET_KEY'),
    amount=amount,
    email=email,
    reference=reference,
    callback_url=os.getenv('PAYSTACK_CALLBACK_URL')
)
```
with:
```python
transaction = PaystackService().initialize_transaction(
    amount=amount, email=email, reference=reference,
)
```

In `payment_callback`, replace:
```python
verification = Transaction.verify(
    key=os.getenv('PAYSTACK_SECRET_KEY'),
    reference=reference
)
```
with:
```python
verification = PaystackService().verify_transaction(reference=reference)
```

Add near your other imports:
```python
from campuslife_services.notifications import NotificationService
```

In `agent_update_vacancy`, replace the whole hardcoded-emails loop:
```python
emails = ['michaelezechukwu0@gmail.com', 'chinenyedavid781@gmail.com', 'jerrychukwu01@gmail.com']
for _ in emails:
    email = EmailMessage(...)
    email.send()
```
with:
```python
NotificationService().notify_admins(
    subject="Agent Vacancy Update",
    body=f"Agent {agent.first_name} {agent.last_name} updated a vacancy for {lodge_name}",
)
```

Do the same in `withdraw` — swap its hardcoded-emails loop for:
```python
NotificationService().notify_admins(
    subject="Agent Withdrawal Request",
    body=f"Agent {agent_name} {agent_lastname} initiated a withdrawal of amount: {balance}",
)
```

`ADMIN_NOTIFICATION_EMAILS` goes in your `.env` (comma-separated) — not in git.

## 5. Frontend wiring (React/Vite)

The `frontend/` service builds your Vite app and serves it through nginx,
which proxies `/api/`, `/admin/`, `/media/`, and `/static/` to the Django
container. This means the browser only ever talks to one origin
(`localhost:3000`), so **you shouldn't need CORS at all** inside Docker —
CORS was only necessary because your Vercel-deployed frontend and
Render/Koyeb-deployed backend were on different domains in production.

Two things to update:

**settings.py — add `localhost` to `ALLOWED_HOSTS`:**
```python
ALLOWED_HOSTS = ['campuslife-c9je.onrender.com', '127.0.0.1', 'localhost', ...]
```
(nginx forwards the original `Host` header, so if you access the app at
`http://localhost:3000`, Django sees `Host: localhost` on the proxied
request and needs to allow it.)

**Frontend API base URL** — find wherever your React code sets the base
URL for API calls (an axios instance, a `fetch` wrapper, a `.env` file
consumed via `import.meta.env.VITE_API_BASE_URL`, etc.) and point it at
`/api` (a relative path) for the Docker build, instead of a hardcoded
`https://campuslife-c9je.onrender.com` or similar. The Dockerfile already
sets `VITE_API_BASE_URL=/api` at build time — but only if your code
actually reads that variable. If it's currently hardcoded as a string
literal somewhere, you'll need to swap that literal for
`import.meta.env.VITE_API_BASE_URL` first.

Also check your Django URL routing: the nginx config assumes your DRF
endpoints are mounted under `/api/` in `djangoProject2/urls.py`. If they're
actually mounted at the root (e.g. `picture_list_api` is just `/pictures/`,
not `/api/pictures/`), adjust the `location /api/` block in
`frontend/nginx.conf` to proxy `location /` instead, or add the `/api/`
prefix in your Django URLconf so the split is clean.
