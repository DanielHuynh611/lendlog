from flask import Blueprint, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os

blueprint = Blueprint('capability_view_loan_list_e3bf329c', __name__)

def get_db_connection():
    """Create and return a database connection."""
    database_url = os.environ.get('DATABASE_URL', 'mysql+pymysql://user:password@localhost/dbname')
    engine = create_engine(database_url, pool_pre_ping=True)
    return engine

@blueprint.get('/api/capability_view_loan_list_e3bf329c/loans')
def get_loans():
    """
    Retrieve all loan records ordered by creation timestamp descending (newest first).
    
    Returns:
        JSON response with list of loans containing id, item_name, borrower_name, and created_at
    
    Error Responses:
        500: Internal server error when database query fails
    """
    try:
        engine = get_db_connection()
        
        with engine.connect() as connection:
            query = text("""
                SELECT id, item_name, borrower_name, created_at
                FROM f_e3bf329c__loans
                ORDER BY created_at DESC
            """)
            
            result = connection.execute(query)
            rows = result.fetchall()
            
            loans = []
            for row in rows:
                loan = {
                    'id': row[0],
                    'item_name': row[1],
                    'borrower_name': row[2],
                    'created_at': row[3].isoformat() if row[3] else None
                }
                loans.append(loan)
            
            return jsonify({'loans': loans}), 200
            
    except SQLAlchemyError as e:
        return jsonify({'error': 'Internal server error when database query fails'}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error when database query fails'}), 500