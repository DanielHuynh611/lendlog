"""Application, optional database, validation and privacy regression checks."""
import pytest
from sqlalchemy import text

from fullstack import create_app

API = '/api/capability_local_browser_storage_03ab1d7c/loans'
OTHER = '/api/capability_record_item_and_borrower_3af7a315/loan-records'
VIEW = '/api/capability_view_loan_list_e3bf329c/loans'


@pytest.fixture
def app():
    application = create_app(testing=True)
    yield application
    application.extensions['database_engine'].dispose()


def post(client, payload, route=API):
    token = client.get(API).json['csrf_token']
    return client.post(route, json=payload, headers={'X-CSRF-Token': token})


def test_main_screen_and_all_assets(app):
    client = app.test_client()
    page = client.get('/')
    assert page.status_code == 200
    assert 'id="loan-form"' in page.text
    assert 'id="loan-list"' in page.text
    assert 'Saved only in this browser' in page.text
    assert page.text.count('class="z-nav-link"') == 1
    assert 'Input field for item name with label' not in page.text
    assert '--z-accent:#ff642f' in page.text
    for asset in ('/static/css/app.css', '/__frontend_assets/frontend/shared/ui/library.js', '/__frontend_assets/frontend/features/local_browser_storage/lendlog.js'):
        assert client.get(asset).status_code == 200
    assert client.get('/__frontend_assets/backend/core/config.py').status_code == 404
    assert "frame-ancestors 'none'" in page.headers['Content-Security-Policy']


def test_frontend_never_uploads_loan_names(app):
    script = app.test_client().get('/__frontend_assets/frontend/features/local_browser_storage/lendlog.js').text
    assert 'localStorage.setItem' in script
    assert 'textContent = value' in script
    assert 'fetch(' not in script
    assert '.innerHTML' not in script


def test_browser_local_mode_without_mysql():
    app = create_app(testing=True, config={'DATABASE_URL': ''})
    client = app.test_client()
    assert client.get('/').status_code == 200
    assert client.get('/health').json['storage'] == 'browser-local'
    assert client.get('/health').json['database'] == 'not-configured'
    assert client.get(API).status_code == 503
    result = app.test_cli_runner().invoke(args=['init-db'])
    assert result.exit_code == 0
    assert 'Browser-local mode' in result.output


def test_api_shared_store_and_private_browser_lists(app):
    alice, bob = app.test_client(), app.test_client()
    created = post(alice, {'item_name': '  Book  ', 'borrower_name': '  Alex  '})
    assert created.status_code == 201
    assert created.json['item_name'] == 'Book'
    assert created.json['borrower_name'] == 'Alex'
    assert alice.get(OTHER).json['loan_records'] == [created.json]
    assert alice.get(VIEW).json['loans'] == [created.json]
    assert bob.get(API).json['loans'] == []
    # Submitted ownership claims cannot select another browser's records.
    response = post(bob, {'item_name': 'Tool', 'borrower_name': 'Sam', 'browser_id': 'somebody-else'})
    assert response.status_code == 201
    assert len(alice.get(API).json['loans']) == 1


@pytest.mark.parametrize('field,value', [
    ('item_name', ''), ('borrower_name', '   '), ('item_name', 123),
    ('borrower_name', None), ('item_name', []), ('item_name', 'x' * 101),
    ('borrower_name', 'x' * 101),
])
def test_api_invalid_names(app, field, value):
    client = app.test_client()
    payload = dict(item_name='Book', borrower_name='Alex')
    payload[field] = value
    response = post(client, payload)
    assert response.status_code == 400
    assert field in response.json['fields']
    assert client.get(API).json['loans'] == []


@pytest.mark.parametrize('payload', [[], None, 'text'])
def test_api_requires_object(app, payload):
    assert post(app.test_client(), payload).status_code == 400


def test_api_duplicates_unicode_and_length_boundary(app):
    client = app.test_client()
    for _ in range(2):
        assert post(client, {'item_name': '文' * 100, 'borrower_name': 'Zoë'}).status_code == 201
    records = client.get(API).json['loans']
    assert len(records) == 2
    assert records[0]['id'] != records[1]['id']


def test_api_csrf_required(app):
    client = app.test_client()
    assert client.post(API, json={'item_name': 'Book', 'borrower_name': 'Alex'}).status_code == 400
    assert client.get(API).json['loans'] == []


def test_init_db_is_repeatable(app):
    client = app.test_client()
    post(client, {'item_name': 'Book', 'borrower_name': 'Alex'})
    runner = app.test_cli_runner()
    for _ in range(2):
        assert runner.invoke(args=['init-db']).exit_code == 0
    assert len(client.get(API).json['loans']) == 1


def test_health_checks_configured_database(app):
    assert app.test_client().get('/health').json['database'] == 'ok'
    with app.extensions['database_engine'].begin() as connection:
        connection.execute(text('SELECT 1'))


def test_no_database_credentials_required_for_local_ui(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', '')
    monkeypatch.setenv('JWT_SECRET', '')
    app = create_app()
    assert app.test_client().get('/').status_code == 200


def test_bad_database_url_is_explained_without_exposing_password(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'not-a-url')
    with pytest.raises(RuntimeError, match='Invalid DATABASE_URL'):
        create_app()


def test_mysql_constraints_measure_characters_not_utf8_bytes():
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects.mysql import dialect
    from backend.core.db import loans
    ddl = str(CreateTable(loans).compile(dialect=dialect()))
    assert 'char_length(trim(item_name))' in ddl
    assert 'char_length(trim(borrower_name))' in ddl


def test_optional_api_survives_restart_with_same_session(tmp_path):
    config = {'DATABASE_URL': 'sqlite+pysqlite:///' + str(tmp_path / 'loans.db')}
    first = create_app(testing=True, config=config)
    client = first.test_client()
    assert post(client, {'item_name': 'Book', 'borrower_name': 'Alex'}).status_code == 201
    cookie = client.get_cookie('lendlog_session')
    first.extensions['database_engine'].dispose()
    second = create_app(testing=True, config=config)
    same_browser = second.test_client()
    same_browser.set_cookie('lendlog_session', cookie.value)
    assert same_browser.get(API).json['loans'][0]['item_name'] == 'Book'
    assert second.test_client().get(API).json['loans'] == []
    second.extensions['database_engine'].dispose()
