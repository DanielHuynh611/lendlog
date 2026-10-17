"""
Flask Blueprint module for recording item and borrower loan records.
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid
import os
from backend.core.db import get_engine
from contextlib import ExitStack as _ConnectionScope

blueprint = Blueprint('capability_record_item_and_borrower_3af7a315', __name__)


@blueprint.post('/api/capability_record_item_and_borrower_3af7a315/loan-records')
def create_loan_record():
    """
    Creates a new loan record with trimmed item name and borrower name,
    generates a unique ID and timestamp, and persists it to storage.
    """
    with _ConnectionScope() as _connection_scope:
        try:
            data = request.get_json()
        
            # Extract fields
            item_name = data.get('item_name')
            borrower_name = data.get('borrower_name')
        
            # Validate that both fields are present
            if item_name is None or borrower_name is None:
                return jsonify({
                    'code': 'VALIDATION_ERROR',
                    'message': 'item_name and borrower_name are required and must not be empty after trimming'
                }), 400
        
            # Trim the fields
            item_name_trimmed = item_name.strip() if isinstance(item_name, str) else ''
            borrower_name_trimmed = borrower_name.strip() if isinstance(borrower_name, str) else ''
        
            # Validate that both fields are not empty after trimming
            if not item_name_trimmed or not borrower_name_trimmed:
                return jsonify({
                    'code': 'VALIDATION_ERROR',
                    'message': 'item_name and borrower_name are required and must not be empty after trimming'
                }), 400
        
            # Generate unique ID and timestamp
            loan_id = str(uuid.uuid4())
            created_at = datetime.utcnow()
        
            # Insert into database
            db = _connection_scope.enter_context(get_engine().connect())
            query = text("""
            INSERT INTO f_3af7a315__loan_records (id, item_name, borrower_name, created_at)
            VALUES (:id, :item_name, :borrower_name, :created_at)
        """)
        
            db.execute(query, {
                'id': loan_id,
                'item_name': item_name_trimmed,
                'borrower_name': borrower_name_trimmed,
                'created_at': created_at
            })
            db.commit()
        
            # Return the created record
            return jsonify({
                'id': loan_id,
                'item_name': item_name_trimmed,
                'borrower_name': borrower_name_trimmed,
                'created_at': created_at.isoformat() + 'Z'
            }), 201
        
        except SQLAlchemyError as e:
            db.rollback()
            return jsonify({
                'code': 'DATABASE_ERROR',
                'message': 'Failed to create loan record'
            }), 500
        except Exception as e:
            return jsonify({
                'code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred'
            }), 500


@blueprint.get('/api/capability_record_item_and_borrower_3af7a315/loan-records')
def get_loan_records():
    """
    Retrieves all loan records ordered by creation timestamp to support
    displaying the list and persistence across browser sessions.
    """
    with _ConnectionScope() as _connection_scope:
        try:
            db = _connection_scope.enter_context(get_engine().connect())
            query = text("""
            SELECT id, item_name, borrower_name, created_at
            FROM f_3af7a315__loan_records
            ORDER BY created_at DESC
        """)
        
            result = db.execute(query)
            rows = result.fetchall()
        
            loan_records = []
            for row in rows:
                loan_records.append({
                    'id': row[0],
                    'item_name': row[1],
                    'borrower_name': row[2],
                    'created_at': row[3].isoformat() + 'Z' if isinstance(row[3], datetime) else row[3]
                })
        
            return jsonify({
                'loan_records': loan_records
            }), 200
        
        except SQLAlchemyError as e:
            return jsonify({
                'code': 'DATABASE_ERROR',
                'message': 'Failed to retrieve loan records'
            }), 500
        except Exception as e:
            return jsonify({
                'code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred'
            }), 500
