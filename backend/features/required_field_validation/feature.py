from flask import Blueprint, request, jsonify
from functools import wraps

blueprint = Blueprint('required_field_validation', __name__)


def validate_required_fields(*fields):
    """
    Decorator to validate that required fields are present and non-empty in request JSON.
    
    Args:
        *fields: Variable number of field names that are required
    
    Returns:
        Decorator function that validates the specified fields
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({
                    'error': 'Content-Type must be application/json',
                    'status': 'error'
                }), 400
            
            data = request.get_json()
            missing_fields = []
            empty_fields = []
            
            for field in fields:
                if field not in data:
                    missing_fields.append(field)
                elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
                    empty_fields.append(field)
            
            if missing_fields or empty_fields:
                error_message = []
                if missing_fields:
                    error_message.append(f"Missing required fields: {', '.join(missing_fields)}")
                if empty_fields:
                    error_message.append(f"Empty required fields: {', '.join(empty_fields)}")
                
                return jsonify({
                    'error': '; '.join(error_message),
                    'status': 'error',
                    'missing_fields': missing_fields,
                    'empty_fields': empty_fields
                }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@blueprint.post('/items')
@validate_required_fields('item_name', 'borrower_name')
def create_item():
    """
    Create a new item with required field validation.
    Requires both item_name and borrower_name to be filled.
    """
    data = request.get_json()
    
    return jsonify({
        'status': 'success',
        'message': 'Item created successfully',
        'data': {
            'item_name': data['item_name'],
            'borrower_name': data['borrower_name']
        }
    }), 201


@blueprint.put('/items/<int:item_id>')
@validate_required_fields('item_name', 'borrower_name')
def update_item(item_id):
    """
    Update an existing item with required field validation.
    Requires both item_name and borrower_name to be filled.
    """
    data = request.get_json()
    
    return jsonify({
        'status': 'success',
        'message': 'Item updated successfully',
        'data': {
            'item_id': item_id,
            'item_name': data['item_name'],
            'borrower_name': data['borrower_name']
        }
    }), 200


@blueprint.post('/validate')
@validate_required_fields('item_name', 'borrower_name')
def validate_fields():
    """
    Validate required fields without persisting data.
    Useful for client-side validation checks.
    """
    data = request.get_json()
    
    return jsonify({
        'status': 'success',
        'message': 'Validation passed',
        'validated_fields': {
            'item_name': data['item_name'],
            'borrower_name': data['borrower_name']
        }
    }), 200


@blueprint.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify({
        'error': 'Bad request',
        'status': 'error'
    }), 400


@blueprint.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500
