"""Safe compatibility APIs. The visible app never uploads its local records."""
import hmac
import secrets
import uuid
from datetime import datetime, timezone

from flask import current_app, jsonify, request, session
from sqlalchemy import insert, select
from backend.core.db import get_engine, loans


def serialize(record):
    return {field: record[field] for field in ('id', 'item_name', 'borrower_name')} | {
        'created_at': record['created_at'].replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')}


def records_response(collection='loans'):
    if current_app.extensions.get('database_engine') is None:
        return jsonify(error='DATABASE_NOT_CONFIGURED', message='This UI uses browser-local storage. Database API mode is not configured.'), 503
    if 'browser_id' not in session:
        session['browser_id'] = str(uuid.uuid4())
        session['csrf_token'] = secrets.token_urlsafe(32)
        session.permanent = True
    owner = session['browser_id']
    engine = get_engine()
    if request.method == 'GET':
        with engine.connect() as connection:
            records = connection.execute(select(loans).where(loans.c.browser_id == owner).order_by(loans.c.created_at.desc(), loans.c.id.desc())).mappings()
            values = [serialize(record) for record in records]
        return jsonify({collection: values, 'csrf_token': session['csrf_token']})
    if not hmac.compare_digest(request.headers.get('X-CSRF-Token', '').encode('utf-8'), session['csrf_token'].encode('utf-8')):
        return jsonify(error='INVALID_CSRF', message='Load the loan list and send its CSRF token before saving.'), 400
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='VALIDATION_ERROR', message='Send item_name and borrower_name as an object.'), 400
    names, errors = {}, {}
    for field in ('item_name', 'borrower_name'):
        value = data.get(field)
        if not isinstance(value, str) or not 1 <= len(value.strip()) <= 100:
            errors[field] = 'Enter 1–100 characters.'
        else:
            names[field] = value.strip()
    if errors:
        return jsonify(error='VALIDATION_ERROR', message='Check the item and borrower names.', fields=errors), 400
    record = dict(id=str(uuid.uuid4()), browser_id=owner, created_at=datetime.now(timezone.utc).replace(tzinfo=None), **names)
    with engine.begin() as connection:
        connection.execute(insert(loans).values(**record))
    return jsonify(serialize(record)), 201
