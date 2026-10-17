"""
Local browser storage feature module for managing loan records.

This module provides endpoints to create and retrieve loan records that are
stored in a MySQL database, designed to work with browser local storage patterns.
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid

blueprint = Blueprint('capability_local_browser_storage_03ab1d7c', __name__)


def get_db_connection():
    """Get database connection from Flask app context."""
    from flask import current_app
    return current_app.config['DATABASE_ENGINE']


@blueprint.post('/api/capability_local_browser_storage_03ab1d7c/loans')
def create_loan_record():
    """
    Create a new loan record in browser local storage with item name, borrower name,
    unique identifier, and creation timestamp.
    
    Returns:
        JSON response with loan record details including id, item_name, borrower_name, and created_at
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'error': 'INVALID_REQUEST',
                'message': 'item_name and borrower_name are required and must not be empty'
            }), 400
        
        item_name = data.get('item_name', '').strip() if data.get('item_name') else ''
        borrower_name = data.get('borrower_name', '').strip() if data.get('borrower_name') else ''
        
        if not item_name or not borrower_name:
            return jsonify({
                'error': 'INVALID_REQUEST',
                'message': 'item_name and borrower_name are required and must not be empty'
            }), 400
        
        # Generate unique ID and timestamp
        loan_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        
        # Insert into database
        engine = get_db_connection()
        with engine.connect() as conn:
            query = text("""
                INSERT INTO f_03ab1d7c__loan_records 
                (id, item_name, borrower_name, created_at)
                VALUES (:id, :item_name, :borrower_name, :created_at)
            """)
            
            conn.execute(query, {
                'id': loan_id,
                'item_name': item_name,
                'borrower_name': borrower_name,
                'created_at': created_at
            })
            conn.commit()
        
        # Return response
        return jsonify({
            'id': loan_id,
            'item_name': item_name,
            'borrower_name': borrower_name,
            'created_at': created_at.isoformat() + 'Z'
        }), 201
        
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'DATABASE_ERROR',
            'message': 'Failed to create loan record'
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred'
        }), 500


@blueprint.get('/api/capability_local_browser_storage_03ab1d7c/loans')
def get_all_loan_records():
    """
    Retrieve all loan records from browser local storage to display the complete
    list of active loans after browser reopening.
    
    Returns:
        JSON response with array of all loan records
    """
    try:
        engine = get_db_connection()
        with engine.connect() as conn:
            query = text("""
                SELECT id, item_name, borrower_name, created_at
                FROM f_03ab1d7c__loan_records
                ORDER BY created_at DESC
            """)
            
            result = conn.execute(query)
            rows = result.fetchall()
            
            loans = []
            for row in rows:
                loans.append({
                    'id': row[0],
                    'item_name': row[1],
                    'borrower_name': row[2],
                    'created_at': row[3].isoformat() + 'Z' if isinstance(row[3], datetime) else row[3]
                })
        
        return jsonify({
            'loans': loans
        }), 200
        
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'DATABASE_ERROR',
            'message': 'Failed to retrieve loan records'
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'INTERNAL_ERROR',
            'message': 'An unexpected error occurred'
        }), 500
