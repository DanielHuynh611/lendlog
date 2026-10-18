"""Private account, loan/history, schema and deployment regression checks."""
import re
from datetime import datetime, timezone, timedelta
import pytest
from sqlalchemy import insert, select, text
from fullstack import create_app
from backend.core.auth import AUTH_COOKIE, issue_token
from backend.core.db import users, loans

API = '/api/loans'
OTHER = '/api/capability_record_item_and_borrower_3af7a315/loan-records'
VIEW = '/api/capability_view_loan_list_e3bf329c/loans'

@pytest.fixture
def app():
    app = create_app(testing=True, config={'SESSION_COOKIE_SECURE': False})
    yield app
    app.extensions['database_engine'].dispose()

def csrf(client, page='/'):
    result = client.get(page)
    return re.search(r'<meta name="csrf-token" content="([^"]+)"', result.text)[1]

def register(client, email='alex@example.com', password='ExamplePassword123', confirmation=None):
    return client.post('/register', data={
        'email': email, 'password': password, 'confirm_password': password if confirmation is None else confirmation,
        'csrf_token': csrf(client, '/register'),
    })

def logged_in(app, email='alex@example.com'):
    client = app.test_client()
    assert register(client, email).status_code == 303
    return client

def post(client, payload, route=API):
    return client.post(route, json=payload, headers={'X-CSRF-Token': csrf(client)})

def test_routes_require_authentication(app):
    client = app.test_client()
    for path in ('/', '/history', '/account'):
        assert client.get(path).headers['Location'] == '/login'
    for path in (API, OTHER, VIEW):
        assert client.get(path).status_code == 401
    assert client.post(API, json={}).status_code == 401

def test_registration_hashes_password_and_sets_cookie(app):
    client = logged_in(app)
    assert client.get_cookie(AUTH_COOKIE)
    with app.extensions['database_engine'].connect() as connection:
        user = connection.execute(select(users)).mappings().one()
    assert user['password_hash'].startswith('pbkdf2_sha256$')
    assert user['password_hash'] != 'ExamplePassword123'
    assert client.get('/').status_code == 200

@pytest.mark.parametrize('email,password,confirmation', [
    ('not-an-email', 'ExamplePassword123', None),
    ('alex@example.com', 'short', None),
    ('alex@example.com', 'ExamplePassword123', 'different'),
    ('alex@example.com', 'x' * 129, None),
])
def test_registration_validation(app, email, password, confirmation):
    client = app.test_client()
    response = register(client, email, password, confirmation)
    assert response.status_code == 400
    assert 'role="alert"' in response.text
    assert client.get_cookie(AUTH_COOKIE) is None

def test_duplicate_email_case_insensitive(app):
    logged_in(app)
    client = app.test_client()
    assert register(client, 'ALEX@example.com').status_code == 409

def test_auth_pages_have_no_navigation(app):
    client = app.test_client()
    for path in ('/register', '/login'):
        page = client.get(path)
        assert page.status_code == 200
        assert '<aside' not in page.text and '<nav' not in page.text
        assert 'data-nav-toggle' not in page.text
        assert 'name="csrf_token"' in page.text

def test_main_screen_navigation_and_assets(app):
    client = logged_in(app)
    for path, name in (('/', 'Loans'), ('/history', 'History')):
        page = client.get(path)
        assert page.status_code == 200
        assert page.text.count('class="z-nav-link"') == 2
        assert '<span>Account</span>' not in page.text
        assert 'href="' + path + '" aria-current="page"' in page.text
        assert '--z-accent:#ff642f' in page.text
        assert "frame-ancestors 'none'" in page.headers['Content-Security-Policy']
    assert 'alex@example.com' in client.get('/').text
    assert client.get('/account').headers['Location'] == '/'
    for asset in ('/static/css/app.css', '/__frontend_assets/frontend/shared/ui/library.js', '/__frontend_assets/frontend/features/local_browser_storage/lendlog.js'):
        assert client.get(asset).status_code == 200
    assert client.get('/__frontend_assets/backend/core/config.py').status_code == 404
    script = client.get('/__frontend_assets/frontend/features/local_browser_storage/lendlog.js').text
    assert 'localStorage.setItem' not in script
    assert '.innerHTML' not in script

def test_login_logout_and_wrong_password(app):
    client = logged_in(app)
    assert client.post('/logout', data={'csrf_token': csrf(client)}).status_code == 303
    assert client.get(API).status_code == 401
    token = csrf(client, '/login')
    assert client.post('/login', data={'email': 'alex@example.com', 'password': 'wrong', 'csrf_token': token}).status_code == 401
    token = csrf(client, '/login')
    assert client.post('/login', data={'email': 'alex@example.com', 'password': 'ExamplePassword123', 'csrf_token': token}).status_code == 303

def test_accounts_isolate_loans_and_ignore_claimed_ownership(app):
    alice, bob = logged_in(app), logged_in(app, 'bob@example.com')
    created = post(alice, {'item_name': '  Book  ', 'borrower_name': '  Sam  ', 'user_id': 'someone-else'})
    assert created.status_code == 201
    assert created.json['item_name'] == 'Book'
    assert created.json['borrower_name'] == 'Sam'
    assert alice.get(OTHER).json['loan_records'] == [created.json]
    assert alice.get(VIEW).json['loans'] == [created.json]
    assert bob.get(API).json['loans'] == []
    assert post(bob, {}, API + '/' + created.json['id'] + '/return').status_code == 404

@pytest.mark.parametrize('field,value', [
    ('item_name', ''), ('borrower_name', '   '), ('item_name', 123),
    ('borrower_name', None), ('item_name', []), ('item_name', 'x' * 101), ('borrower_name', 'x' * 101),
])
def test_invalid_names(app, field, value):
    client = logged_in(app)
    payload = dict(item_name='Book', borrower_name='Alex')
    payload[field] = value
    response = post(client, payload)
    assert response.status_code == 400
    assert field in response.json['fields']
    assert client.get(API).json['loans'] == []

@pytest.mark.parametrize('payload', [[], None, 'text'])
def test_requires_object(app, payload):
    assert post(logged_in(app), payload).status_code == 400

def test_duplicate_names_and_unicode_boundary(app):
    client = logged_in(app)
    for _ in range(2):
        assert post(client, {'item_name': '文' * 100, 'borrower_name': 'Zoë'}).status_code == 201
    records = client.get(API).json['loans']
    assert len(records) == 2
    assert records[0]['id'] != records[1]['id']

def test_return_moves_owned_loan_to_history(app):
    client = logged_in(app)
    created = post(client, {'item_name': 'Book', 'borrower_name': 'Sam'}).json
    path = API + '/' + created['id'] + '/return'
    result = post(client, {}, path)
    assert result.status_code == 200
    assert result.json['status'] == 'returned'
    assert result.json['returned_at']
    assert client.get(API + '?status=active').json['loans'] == []
    assert client.get(API + '?status=returned').json['loans'] == [result.json]
    assert post(client, {}, path).status_code == 409
    assert post(client, {}, API + '/missing/return').status_code == 404
    assert client.get(API + '?status=invalid').status_code == 400

def test_csrf_protects_mutations(app):
    client = logged_in(app)
    assert client.post(API, json={'item_name': 'Book', 'borrower_name': 'Sam'}).status_code == 400
    assert client.post('/logout').status_code == 400
    assert client.get(API).json['loans'] == []

def test_invalid_expired_and_wrong_issuer_tokens(app):
    for token in ('broken', None):
        client = app.test_client()
        if token:
            client.set_cookie(AUTH_COOKIE, token)
        assert client.get(API).status_code == 401
    with app.app_context():
        expired = issue_token('unknown', expires_in_seconds=-1)
    client = app.test_client()
    client.set_cookie(AUTH_COOKIE, expired)
    assert client.get(API).status_code == 401
    import jwt
    with app.app_context():
        wrong_issuer = jwt.encode({'sub': 'unknown', 'iss': 'wrong', 'iat': datetime.now(timezone.utc), 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, app.config['JWT_SECRET'], algorithm='HS256')
    client.set_cookie(AUTH_COOKIE, wrong_issuer)
    assert client.get(API).status_code == 401

def test_health_and_repeated_init_db(app):
    client = logged_in(app)
    post(client, {'item_name': 'Book', 'borrower_name': 'Sam'})
    assert client.get('/health').json['database'] == 'ok'
    for _ in range(2):
        assert app.test_cli_runner().invoke(args=['init-db']).exit_code == 0
    assert len(client.get(API).json['loans']) == 1

def test_old_browser_api_table_is_preserved(app):
    with app.extensions['database_engine'].begin() as connection:
        connection.execute(text('CREATE TABLE loan_records (id TEXT PRIMARY KEY)'))
        connection.execute(text("INSERT INTO loan_records (id) VALUES ('legacy')"))
    assert app.test_cli_runner().invoke(args=['init-db']).exit_code == 0
    with app.extensions['database_engine'].connect() as connection:
        assert connection.execute(text('SELECT id FROM loan_records')).scalar_one() == 'legacy'

def test_mysql_constraints_measure_characters():
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects.mysql import dialect
    ddl = str(CreateTable(loans).compile(dialect=dialect()))
    assert 'char_length(trim(item_name))' in ddl
    assert 'char_length(trim(borrower_name))' in ddl

def test_persistence_and_second_device_login(tmp_path):
    config = {'DATABASE_URL': 'sqlite+pysqlite:///' + str(tmp_path / 'loans.db'), 'SESSION_COOKIE_SECURE': False}
    first = create_app(testing=True, config=config)
    client = logged_in(first)
    record = post(client, {'item_name': 'Book', 'borrower_name': 'Sam'}).json
    post(client, {}, API + '/' + record['id'] + '/return')
    first.extensions['database_engine'].dispose()
    second = create_app(testing=True, config=config)
    other_device = second.test_client()
    token = csrf(other_device, '/login')
    assert other_device.post('/login', data={'email': 'alex@example.com', 'password': 'ExamplePassword123', 'csrf_token': token}).status_code == 303
    assert other_device.get(API + '?status=returned').json['loans'][0]['id'] == record['id']
    second.extensions['database_engine'].dispose()

def test_secure_cookie_configuration():
    app = create_app(testing=True, config={'SESSION_COOKIE_SECURE': True})
    client = app.test_client()
    response = register(client)
    assert any(cookie.startswith(AUTH_COOKIE + '=') and 'Secure' in cookie and 'HttpOnly' in cookie for cookie in response.headers.getlist('Set-Cookie'))
    app.extensions['database_engine'].dispose()

def test_required_config_explains_missing_database(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', '')
    with pytest.raises(RuntimeError, match='DATABASE_URL is required'):
        create_app()

def test_invalid_database_url_explained(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'not-a-url')
    with pytest.raises(RuntimeError, match='Invalid DATABASE_URL'):
        create_app()

@pytest.mark.parametrize('host', ['localhost', '127.0.0.1', '[::1]'])
def test_passwordless_loopback_requires_explicit_opt_in(monkeypatch, host):
    from backend.core.config import get_settings
    monkeypatch.setenv('DATABASE_URL', 'mysql+mysqlconnector://root@' + host + ':3306/lendlog')
    monkeypatch.setenv('JWT_SECRET', 'test-only-secret-at-least-32-characters')
    monkeypatch.setenv('ALLOW_PASSWORDLESS_LOCAL_DB', 'false')
    with pytest.raises(RuntimeError, match='requires a password'):
        get_settings()
    monkeypatch.setenv('ALLOW_PASSWORDLESS_LOCAL_DB', 'true')
    assert get_settings().database_url.startswith('mysql+mysqlconnector://root@')

@pytest.mark.parametrize('host', ['db.example.com', '192.168.1.20', 'localhost.example.com'])
def test_passwordless_remote_database_always_rejected(monkeypatch, host):
    from backend.core.config import get_settings
    monkeypatch.setenv('DATABASE_URL', 'mysql+mysqlconnector://root@' + host + ':3306/lendlog')
    monkeypatch.setenv('ALLOW_PASSWORDLESS_LOCAL_DB', 'true')
    monkeypatch.setenv('JWT_SECRET', 'test-only-secret-at-least-32-characters')
    with pytest.raises(RuntimeError, match='requires a password'):
        get_settings()


def mutate(client, method, path, payload=None):
    return client.open(path, method=method, json=payload, headers={'X-CSRF-Token': csrf(client)})


def test_restore_returns_loan_to_original_state(app):
    client = logged_in(app)
    created = post(client, {'item_name': 'Drill', 'borrower_name': 'Sam'}).json
    path = API + '/' + created['id']
    assert post(client, {}, path + '/return').status_code == 200
    restored = post(client, {}, path + '/restore')
    assert restored.status_code == 200
    assert restored.json == created
    assert client.get(API + '?status=returned').json['loans'] == []
    assert client.get(API + '?status=active').json['loans'] == [created]
    assert post(client, {}, path + '/restore').status_code == 409
    assert post(client, {}, path + '/return').status_code == 200


@pytest.mark.parametrize('returned', [False, True])
def test_edit_preserves_record_status_dates_and_owner(app, returned):
    client = logged_in(app)
    created = post(client, {'item_name': 'Book', 'borrower_name': 'Sam'}).json
    path = API + '/' + created['id']
    before = post(client, {}, path + '/return').json if returned else created
    response = mutate(client, 'PATCH', path, {'item_name': '  Revised book  ', 'borrower_name': '  Zoë  ', 'status': 'active', 'user_id': 'not-owner'})
    assert response.status_code == 200
    assert response.json['item_name'] == 'Revised book'
    assert response.json['borrower_name'] == 'Zoë'
    for field in ('id', 'status', 'created_at', 'returned_at'):
        assert response.json[field] == before[field]
    assert client.get(API).json['loans'] == [response.json]


@pytest.mark.parametrize('payload', [None, [], 'text', {}, {'item_name': '', 'borrower_name': 'Sam'}, {'item_name': 'Book', 'borrower_name': 'x' * 101}])
def test_edit_validation_does_not_change_existing_record(app, payload):
    client = logged_in(app)
    created = post(client, {'item_name': 'Book', 'borrower_name': 'Sam'}).json
    response = mutate(client, 'PATCH', API + '/' + created['id'], payload)
    assert response.status_code == 400
    assert client.get(API).json['loans'] == [created]


@pytest.mark.parametrize('returned', [False, True])
def test_delete_removes_only_selected_owned_record(app, returned):
    client = logged_in(app)
    first = post(client, {'item_name': 'Book', 'borrower_name': 'Sam'}).json
    second = post(client, {'item_name': 'Book', 'borrower_name': 'Sam'}).json
    path = API + '/' + first['id']
    if returned:
        post(client, {}, path + '/return')
    assert mutate(client, 'DELETE', path).status_code == 204
    assert client.get(API).json['loans'] == [second]
    assert mutate(client, 'DELETE', path).status_code == 404


@pytest.mark.parametrize('method,suffix', [('PATCH', ''), ('DELETE', ''), ('POST', '/restore'), ('POST', '/return')])
def test_all_record_actions_require_owner(app, method, suffix):
    alice, bob = logged_in(app), logged_in(app, 'bob@example.com')
    created = post(alice, {'item_name': 'Book', 'borrower_name': 'Sam'}).json
    path = API + '/' + created['id'] + suffix
    response = mutate(bob, method, path, {'item_name': 'Changed', 'borrower_name': 'Unknown'})
    assert response.status_code == 404
    assert alice.get(API).json['loans'] == [created]
    assert app.test_client().open(path, method=method).status_code == 401


@pytest.mark.parametrize('method,suffix', [('PATCH', ''), ('DELETE', ''), ('POST', '/restore'), ('POST', '/return')])
def test_all_record_actions_require_csrf(app, method, suffix):
    client = logged_in(app)
    created = post(client, {'item_name': 'Book', 'borrower_name': 'Sam'}).json
    response = client.open(API + '/' + created['id'] + suffix, method=method, json={'item_name': 'Changed', 'borrower_name': 'Unknown'})
    assert response.status_code == 400
    assert client.get(API).json['loans'] == [created]
