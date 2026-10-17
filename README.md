# LendLog

A small, no-account loan list. Enter an item and borrower, save, and view the
newest entries first. Names are required and limited to 100 characters.

The visible application stores records **only in this browser's local storage**.
It does not upload loan names. Refreshing or reopening the same browser preserves
them; another browser/device starts empty. Clearing site data removes them.
Anyone using the same browser profile can see them. There is no edit, delete,
return tracking, account, synchronisation, export or backup workflow.

## Run locally

```bash
cd /Users/danielhuynh/Desktop/comp3850/lendlog-fullstack
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
flask --app 'fullstack:create_app()' run --debug --port 5001
```

Open http://127.0.0.1:5001/. No database or secrets are required for browser-local
mode. Use localhost or HTTPS; the app uses browser cryptography for record IDs.

```bash
python -m pytest -q
```

Test: save an item/borrower, refresh, reopen the same browser, check two records
with identical names, and confirm blank names are rejected. A different browser
profile should have an empty list.

## AWS deployment

The supplied files follow `deployment-guide` and assume a **separate EC2 instance**,
repository directory `/home/ubuntu/lendlog`, and Gunicorn port 8000.
Do not replace the existing apps or their DNS records. If sharing an instance,
choose an unused port in BOTH the service and Nginx configurations.

Authorize this private repository with a read-only deploy key as in the guide:

```bash
git clone git@github.com:DanielHuynh611/lendlog.git
cd lendlog
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create `.env` using your editor, copying the keys in `.env.example`. For the
browser-local app, keep `DATABASE_URL=` and `JWT_SECRET=` blank. Database setup
steps in the guide are optional for this mode; the Flask stack and MySQL
compatibility are retained. No database worker or MySQL service is needed to
serve the browser-local UI.

```bash
chmod 600 .env
python -m pytest -q
flask --app 'fullstack:create_app()' init-db
flask --app 'fullstack:create_app()' routes
sudo cp deploy/lendlog.service /etc/systemd/system/lendlog.service
sudo systemctl daemon-reload
sudo systemctl enable --now lendlog
curl -fsS --retry 5 --retry-delay 2 --retry-connrefused http://127.0.0.1:8000/health
```

Require a successful health check, not just an 'active' service status.

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/lendlog
sudo ln -s /etc/nginx/sites-available/lendlog /etc/nginx/sites-enabled/lendlog
sudo nginx -t
sudo systemctl reload nginx
curl -fsS -H 'Host: lendlog.track-my-habit.me' http://127.0.0.1/health
```

In Namecheap add one A record: Host `lendlog`, Value the new EC2 **Elastic IP**,
TTL Automatic. Keep `@`, `www` and `daily-win` unchanged. Ensure the EC2 security
group permits HTTP 80 and HTTPS 443, not public 8000 or 3306.

```bash
nslookup lendlog.track-my-habit.me
sudo snap install --classic certbot
sudo /snap/bin/certbot --nginx -d lendlog.track-my-habit.me
curl -fsS https://lendlog.track-my-habit.me/health
sudo /snap/bin/certbot renew --dry-run
```

After HTTPS works, set `COOKIE_SECURE=true` in `.env` and restart:
`sudo systemctl restart lendlog`. Test saving and reloading on the final HTTPS
hostname. HTTP, HTTPS, localhost, an IP address and different ports have separate
browser storage; test records created before the final URL do not transfer.

After a reboot, verify `systemctl is-active lendlog nginx` and the public health
endpoint. Check logs with `sudo journalctl -u lendlog -n 60 --no-pager`.

For later updates:

```bash
cd /home/ubuntu/lendlog
git pull --ff-only origin main
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
sudo systemctl restart lendlog
curl -fsS --retry 5 --retry-delay 2 --retry-connrefused http://127.0.0.1:8000/health
```

## Optional MySQL compatibility

The generated API routes remain, but are **not used by the visible loan list**.
They share one SQLAlchemy Core/MySQL table, isolate data by signed browser
session and require CSRF tokens for writes. There is no account recovery:
clearing the session cookie loses API access to that browser's server records.
Do not use this optional API as a recovery or sync mechanism for the local UI.

To exercise the database steps in the deployment guide, create a fresh MySQL
database and user, then configure actual credentials and a random secret:

```dotenv
DATABASE_URL=mysql+mysqlconnector://YOUR_USER:YOUR_PASSWORD@localhost:3306/YOUR_DATABASE
JWT_SECRET=YOUR_RANDOM_SECRET_AT_LEAST_32_CHARACTERS
JWT_ISSUER=zorentia-app
COOKIE_SECURE=false
```

Generate the secret privately with `openssl rand -hex 32`. URL-encode special
characters in the password; replace every placeholder. Do not post secrets or
commit `.env`. Run `flask --app 'fullstack:create_app()' init-db` to create missing
tables, or apply `database/schema.sql` to a fresh database. This is not a migration
for the original three generated tables. Existing unrelated tables are not
deleted. MySQL timestamps use UTC.

With a configured database, `/health` checks connectivity and returns 503 on
failure. Without one, it reports browser-local mode. If a terminal variable
overrides `.env`, unset that variable and retry. The sample service can add
`Wants=mysql.service` and `After=mysql.service` to its Unit section in database mode.

Earlier generated verification reports/manifests are historical snapshots, not
claims that the improved implementation has passed those original checks.
