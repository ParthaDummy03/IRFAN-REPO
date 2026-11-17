# Taza Food Corner upgrade

## Changes
- `store/cart.py`: fixed missing request argument and subtotal NameError.
- `store/assistant.py`, `store/assistant_views.py`, `store/static/store/assistant.js`: Bangla menu assistant. With `OPENAI_API_KEY`, it uses a model for natural-language recommendations; without one, a menu-backed recommendation fallback works. No automated checkout or payment.
- `render.yaml`, `build.sh`, `config/settings.py`: Render Web Service + PostgreSQL deployment configuration.
- `requirements.txt`: dependencies for Python 3.11 (Django 5.2 LTS); install using `pip install -r requirements.txt`.

## Local (Windows PowerShell)
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py test store
python manage.py runserver
```

## Render
1. Push project source to GitHub without `.venv`, `.env`, `db.sqlite3`, `.git` from this ZIP, or credentials.
2. In Render select New > Blueprint, choose repository and use `render.yaml`. Confirm database plan/cost/availability before applying.
3. When provisioned, visit the assigned `.onrender.com` hostname. Render sets `DATABASE_URL`, host, `DJANGO_SECRET_KEY`, and `DJANGO_DEBUG=False`.
4. Optionally configure `OPENAI_API_KEY` as a secret in Render environment to enable model-backed chat. Without it, menu-based chat still functions. `OPENAI_MODEL` defaults to `gpt-4.1-mini`.
5. Run `python manage.py seed_demo` on the deployed database if you want demo products (this is NOT run automatically). Add real products in Django admin.

**Important:** Hosted SQLite is not persistent on ephemeral Render filesystems. Use Render PostgreSQL for durable cart-session storage and products. Verify that the desired database plan is available and priced appropriately. The assistant is not authorized to access customer accounts or make purchases. For real production use, replace in-memory chat throttling with shared cache (e.g. Redis), confirm provider costs, and add monitoring.
