"""One pooled engine and one loan store for the optional generated APIs."""
import click
from flask import current_app
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, MetaData, String, Table, column, create_engine, event, func
from sqlalchemy.pool import StaticPool

metadata = MetaData()
users = Table(
    'lendlog_users', metadata,
    Column('id', String(36), primary_key=True),
    Column('email', String(254), nullable=False, unique=True),
    Column('password_hash', String(255), nullable=False),
    Column('created_at', DateTime, nullable=False),
)
loans = Table(
    'lendlog_loans', metadata,
    Column('id', String(36), primary_key=True),
    Column('user_id', String(36), ForeignKey('lendlog_users.id'), nullable=False),
    Column('item_name', String(100), nullable=False),
    Column('borrower_name', String(100), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('status', String(16), nullable=False, server_default='active'),
    Column('returned_at', DateTime, nullable=True),
    CheckConstraint(func.char_length(func.trim(column('item_name'))).between(1, 100), name='ck_loan_item'),
    CheckConstraint(func.char_length(func.trim(column('borrower_name'))).between(1, 100), name='ck_loan_borrower'),
    CheckConstraint("status IN ('active', 'returned')", name='ck_loan_status'),
    CheckConstraint("(status = 'active' AND returned_at IS NULL) OR (status = 'returned' AND returned_at IS NOT NULL)", name='ck_loan_return_date'),
    Index('ix_lendlog_user_status_created', 'user_id', 'status', 'created_at'),
)

def configure_database(app):
    url = app.config.get('DATABASE_URL')
    engine = None
    if url:
        options = {'pool_pre_ping': True}
        if url.startswith('sqlite'):
            options['connect_args'] = {'check_same_thread': False}
            if ':memory:' in url:
                options['poolclass'] = StaticPool
        else:
            options.update(pool_size=2, max_overflow=1, pool_recycle=1800, connect_args={'connection_timeout': 5})
        engine = create_engine(url, **options)
        if engine.dialect.name == 'sqlite':
            @event.listens_for(engine, 'connect')
            def foreign_keys(connection, _record):
                connection.execute('PRAGMA foreign_keys=ON')
        if engine.dialect.name == 'mysql':
            @event.listens_for(engine, 'connect')
            def utc(connection, _record):
                cursor = connection.cursor()
                cursor.execute("SET time_zone = '+00:00'")
                cursor.close()
        if app.testing:
            metadata.create_all(engine)
    app.extensions['database_engine'] = engine
    app.config['DATABASE_ENGINE'] = engine

    @app.cli.command('init-db')
    def init_db():
        if engine is None:
            click.echo('Browser-local mode: no database is configured or needed by the UI.')
        else:
            metadata.create_all(engine)
            click.echo('LendLog database tables are ready. Existing records were preserved.')

def get_engine():
    engine = current_app.extensions.get('database_engine')
    if engine is None:
        raise RuntimeError('database_not_configured')
    return engine
