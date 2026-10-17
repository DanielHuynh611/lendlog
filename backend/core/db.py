"""One pooled engine and one loan store for the optional generated APIs."""
import click
from flask import current_app
from sqlalchemy import CheckConstraint, Column, DateTime, Index, MetaData, String, Table, column, create_engine, event, func
from sqlalchemy.pool import StaticPool

metadata = MetaData()
loans = Table(
    'loan_records', metadata,
    Column('id', String(36), primary_key=True),
    Column('browser_id', String(36), nullable=False),
    Column('item_name', String(100), nullable=False),
    Column('borrower_name', String(100), nullable=False),
    Column('created_at', DateTime, nullable=False),
    CheckConstraint(func.char_length(func.trim(column('item_name'))).between(1, 100), name='ck_loan_item'),
    CheckConstraint(func.char_length(func.trim(column('borrower_name'))).between(1, 100), name='ck_loan_borrower'),
    Index('ix_loan_browser_created', 'browser_id', 'created_at'),
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
