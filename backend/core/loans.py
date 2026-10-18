"""Account-owned loan recording, listing and return history."""
import uuid
from datetime import datetime, timezone

from flask import g, jsonify, request
from sqlalchemy import delete, insert, select, update
from backend.core.auth import require_auth
from backend.core.db import get_engine, loans


def serialize(record):
    values = {field: record[field] for field in ('id', 'item_name', 'borrower_name', 'status')}
    for field in ('created_at', 'returned_at'):
        value = record[field]
        values[field] = value.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') if value else None
    return values


@require_auth
def records_response(collection='loans'):
    engine = get_engine()
    if request.method == 'GET':
        status = request.args.get('status', 'all')
        if status not in {'active', 'returned', 'all'}:
            return jsonify(error='INVALID_STATUS', message='Choose active, returned or all loans.'), 400
        query = select(loans).where(loans.c.user_id == g.user['id'])
        if status != 'all':
            query = query.where(loans.c.status == status)
        order = loans.c.returned_at.desc() if status == 'returned' else loans.c.created_at.desc()
        with engine.connect() as connection:
            values = [serialize(row) for row in connection.execute(query.order_by(order, loans.c.created_at.desc(), loans.c.id.desc())).mappings()]
        return jsonify({collection: values})
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
    record = dict(id=str(uuid.uuid4()), user_id=g.user['id'], status='active', returned_at=None,
                  created_at=datetime.now(timezone.utc).replace(tzinfo=None), **names)
    with engine.begin() as connection:
        connection.execute(insert(loans).values(**record))
    return jsonify(serialize(record)), 201


@require_auth
def return_response(loan_id):
    return status_response(loan_id, 'returned')


@require_auth
def restore_response(loan_id):
    return status_response(loan_id, 'active')


def status_response(loan_id, target):
    previous = 'active' if target == 'returned' else 'returned'
    with get_engine().begin() as connection:
        changed = connection.execute(update(loans).where(
            loans.c.id == loan_id, loans.c.user_id == g.user['id'], loans.c.status == previous
        ).values(status=target, returned_at=datetime.now(timezone.utc).replace(tzinfo=None) if target == 'returned' else None))
        row = connection.execute(select(loans).where(loans.c.id == loan_id, loans.c.user_id == g.user['id'])).mappings().first()
        if row is None:
            return jsonify(error='NOT_FOUND', message='Loan not found.'), 404
        if changed.rowcount == 0:
            return jsonify(error='STATUS_CHANGED', message='This loan is already ' + ('returned.' if target == 'returned' else 'outstanding. Refresh the list.')), 409
        return jsonify(serialize(row))


@require_auth
def edit_response(loan_id):
    with get_engine().begin() as connection:
        owned = connection.execute(select(loans).where(
            loans.c.id == loan_id, loans.c.user_id == g.user['id']
        ).with_for_update()).mappings().first()
        if owned is None:
            return jsonify(error='NOT_FOUND', message='Loan not found.'), 404
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error='VALIDATION_ERROR', message='Send an item and borrower name.'), 400
        names, errors = {}, {}
        for field in ('item_name', 'borrower_name'):
            value = data.get(field)
            if not isinstance(value, str) or not 1 <= len(value.strip()) <= 100:
                errors[field] = 'Enter 1–100 characters.'
            else:
                names[field] = value.strip()
        if errors:
            return jsonify(error='VALIDATION_ERROR', message='Check the item and borrower names.', fields=errors), 400
        connection.execute(update(loans).where(loans.c.id == loan_id, loans.c.user_id == g.user['id']).values(**names))
        row = connection.execute(select(loans).where(loans.c.id == loan_id, loans.c.user_id == g.user['id'])).mappings().one()
        return jsonify(serialize(row))


@require_auth
def delete_response(loan_id):
    with get_engine().begin() as connection:
        removed = connection.execute(delete(loans).where(loans.c.id == loan_id, loans.c.user_id == g.user['id']))
        if removed.rowcount == 0:
            return jsonify(error='NOT_FOUND', message='Loan not found.'), 404
    return '', 204
