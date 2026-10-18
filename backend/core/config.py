"""Load project-root settings for Flask, Gunicorn and systemd."""
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

@dataclass(frozen=True)
class Settings:
    database_url: str
    jwt_secret: str
    jwt_issuer: str

def get_settings():
    load_dotenv(Path(__file__).resolve().parents[2] / '.env', override=False)
    url = os.getenv('DATABASE_URL', '').strip()
    secret = os.getenv('JWT_SECRET', '').strip()
    if not url:
        raise RuntimeError('DATABASE_URL is required for accounts. Configure the project .env file with your MySQL credentials.')
    if url:
        try:
            parsed = make_url(url)
        except ArgumentError:
            raise RuntimeError('Invalid DATABASE_URL. Use mysql+mysqlconnector://USER:PASSWORD@localhost:3306/DATABASE; URL-encode password punctuation.') from None
        if parsed.drivername != 'mysql+mysqlconnector':
            raise RuntimeError('DATABASE_URL must use mysql+mysqlconnector.')
        if not parsed.database or not parsed.username:
            raise RuntimeError('DATABASE_URL needs a username and database name.')
        passwordless_local = (
            os.getenv('ALLOW_PASSWORDLESS_LOCAL_DB', 'false').lower() == 'true'
            and parsed.host in {'localhost', '127.0.0.1', '::1'}
        )
        if not parsed.password and not passwordless_local:
            raise RuntimeError('DATABASE_URL requires a password. For passwordless local development only, use a loopback host and ALLOW_PASSWORDLESS_LOCAL_DB=true.')
        if not secret or len(secret) < 32 or secret.startswith('replace-'):
            raise RuntimeError('Set JWT_SECRET in .env to a random secret of at least 32 characters.')
    return Settings(url, secret, os.getenv('JWT_ISSUER', 'zorentia-app'))
