# LendLog

Private loan tracking with **Loans** and **History** screens.
Register/sign in, record an item and borrower, and mark it returned to move it
into History. Use **Mark outstanding** in History to move it back to Loans.
Both lists provide **Edit** and **Delete** actions; deletion requires confirmation
and is permanent. The original orange/dark styling and sidebar are retained.
Authentication pages have no navigation sidebar.

Flask, vanilla JavaScript, SQLAlchemy Core/MySQL and Gunicorn remain the stack.
Passwords are hashed; signed HttpOnly bearer cookies and CSRF checks protect
browser requests. Loans and history are stored against the authenticated user,
not a browser identifier or client-supplied user ID.

## Run locally

Create a MySQL database and user with access to that database. In VS Code,
create `.env` at the project root, using the keys in `.env.example`:

```dotenv
DATABASE_URL=mysql+mysqlconnector://YOUR_USER:YOUR_PASSWORD@localhost:3306/YOUR_DATABASE
JWT_SECRET=YOUR_RANDOM_SECRET_AT_LEAST_32_CHARACTERS
JWT_ISSUER=zorentia-app
COOKIE_SECURE=false
```

Replace every placeholder with your actual values. Generate the secret privately
with `openssl rand -hex 32`. URL-encode special password characters in the URL.
Do not commit or share `.env`. Existing exported variables override this file.

For passwordless **local development only**, if `mysql -u root` already works
without a password, create a dedicated local database and set these in `.env`:

```dotenv
DATABASE_URL=mysql+mysqlconnector://root@127.0.0.1:3306/lendlog
ALLOW_PASSWORDLESS_LOCAL_DB=true
```

Keep a valid random `JWT_SECRET`. This opt-in does not reset MySQL credentials
or make an existing password-protected user passwordless. Do not use it on AWS;
use the password-protected database user from the deployment guide there.

```bash
cd /Users/danielhuynh/Desktop/comp3850/lendlog-fullstack
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
flask --app 'fullstack:create_app()' init-db
flask --app 'fullstack:create_app()' run --debug --port 5001
```

Open http://127.0.0.1:5001/register. Use an unused email and an 8–128 character
password, confirmed twice. Save and edit a loan, mark it returned, open History,
and mark it outstanding again. Check Cancel before confirming a deletion.
Sign out from the sidebar and sign in again. Another account must not see your records.

```bash
python -m pytest -q
```

Tests use isolated SQLite databases, including a file-backed restart check.
The core account and record workflows were also checked against an isolated
local MySQL database. Verify `init-db`, `/health` and registration on your
deployment server as well.

## Existing data

Run `init-db` before starting the updated version. It creates `lendlog_users`
and `lendlog_loans` without deleting the old `loan_records` table or original
generated tables. `database/schema.sql` provides equivalent fresh-install SQL.

Earlier browser-local records remain in that browser and are not automatically
uploaded, deleted or assigned to a new account. Legacy anonymous API records
also remain untouched but are not exposed through the new account APIs.
There is no automatic migration because those records have no verified owner.

## AWS EC2

Follow `deployment-guide` with these project-specific values:

- Repository: `git@github.com:DanielHuynh611/lendlog.git` (private; add a read-only deploy key).
- Project root: `/home/ubuntu/lendlog`.
- Service: **lendlog** throughout, not myapp or daily-win.
- Proposed subdomain: `lendlog.track-my-habit.me`.
- Gunicorn: one worker, two threads, private port 8000 on a separate instance.

Install MySQL/Python/Nginx using the guide, create the database/user and configure
the project-root `.env` as above. Then:

```bash
cd /home/ubuntu/lendlog
source .venv/bin/activate
python -m pip install -r requirements.txt
chmod 600 .env
python -m pytest -q
flask --app 'fullstack:create_app()' init-db
flask --app 'fullstack:create_app()' routes
sudo cp deploy/lendlog.service /etc/systemd/system/lendlog.service
sudo systemctl daemon-reload
sudo systemctl enable --now lendlog
sudo systemctl restart lendlog
curl -fsS --retry 5 --retry-delay 2 --retry-connrefused http://127.0.0.1:8000/health
```

Stop if setup or health checks fail. 'Active' alone is not a database-readiness check.

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/lendlog
sudo ln -s /etc/nginx/sites-available/lendlog /etc/nginx/sites-enabled/lendlog
sudo nginx -t
sudo systemctl reload nginx
```

Add an A record with Host `lendlog`, Value the new instance's **Elastic IP**,
TTL Automatic. Keep existing `@`, `www` and `daily-win` records unchanged.
Allow inbound ports 80 and 443, not public 8000 or 3306.

```bash
nslookup lendlog.track-my-habit.me
sudo snap install --classic certbot
sudo /snap/bin/certbot --nginx -d lendlog.track-my-habit.me
curl -fsS https://lendlog.track-my-habit.me/health
sudo /snap/bin/certbot renew --dry-run
```

After HTTPS succeeds, set `COOKIE_SECURE=true` in `.env` and restart lendlog.
Test registration, saving, editing, return/restore, deletion and sign-in
again at the public HTTPS URL. Open the URL directly in a browser, not through
Slack's sandboxed PDF preview.

On a shared EC2 instance, use a free Gunicorn port in both deployment files and
a separate database. Do not overwrite another app's service, site or DNS record.

For later updates:

```bash
cd /home/ubuntu/lendlog
git pull --ff-only origin main
source .venv/bin/activate
python -m pip install -r requirements.txt
flask --app 'fullstack:create_app()' init-db
sudo systemctl restart lendlog
curl -fsS --retry 5 --retry-delay 2 --retry-connrefused http://127.0.0.1:8000/health
```

After reboot, verify `systemctl is-active mysql lendlog nginx` and public health.
Logs: `sudo journalctl -u lendlog -n 60 --no-pager`.

This small release has no email verification, password reset, account deletion
or password-change workflow. Sign-out clears browser authentication; previously
issued tokens remain valid until expiry (24 hours). These are limitations, not
claims of comprehensive production security. Earlier generated reports and
manifests are historical snapshots; use the current README and tests.
