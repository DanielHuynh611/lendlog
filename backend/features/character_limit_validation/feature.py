"""
Character limit validation module for Flask application.

This module provides validation utilities to limit item name and borrower name
to 100 characters maximum.
"""

from flask import Blueprint, request, jsonify
from functools import wraps


blueprint = Blueprint('character_limit_validation', __name__)


# Constants
MAX_ITEM_NAME_LENGTH = 100
MAX_BORROWER_NAME_LENGTH = 100


class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(self.message)


def validate_item_name(item_name):
    """
    Validate that item name does not exceed maximum character limit.
    
    Args:
        item_name: The item name to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If item name exceeds maximum length
    """
    if item_name is None:
        raise ValidationError("Item name cannot be None", field="item_name")
    
    if not isinstance(item_name, str):
        raise ValidationError("Item name must be a string", field="item_name")
    
    if len(item_name) > MAX_ITEM_NAME_LENGTH:
        raise ValidationError(
            f"Item name must not exceed {MAX_ITEM_NAME_LENGTH} characters",
            field="item_name"
        )
    
    return True


def validate_borrower_name(borrower_name):
    """
    Validate that borrower name does not exceed maximum character limit.
    
    Args:
        borrower_name: The borrower name to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If borrower name exceeds maximum length
    """
    if borrower_name is None:
        raise ValidationError("Borrower name cannot be None", field="borrower_name")
    
    if not isinstance(borrower_name, str):
        raise ValidationError("Borrower name must be a string", field="borrower_name")
    
    if len(borrower_name) > MAX_BORROWER_NAME_LENGTH:
        raise ValidationError(
            f"Borrower name must not exceed {MAX_BORROWER_NAME_LENGTH} characters",
            field="borrower_name"
        )
    
    return True


def validate_character_limits(data):
    """
    Validate character limits for item name and borrower name in data dictionary.
    
    Args:
        data: Dictionary containing item_name and/or borrower_name fields
        
    Returns:
        tuple: (is_valid, errors) where is_valid is bool and errors is dict
    """
    errors = {}
    
    if 'item_name' in data:
        try:
            validate_item_name(data['item_name'])
        except ValidationError as e:
            errors['item_name'] = e.message
    
    if 'borrower_name' in data:
        try:
            validate_borrower_name(data['borrower_name'])
        except ValidationError as e:
            errors['borrower_name'] = e.message
    
    return (len(errors) == 0, errors)


def require_character_limit_validation(f):
    """
    Decorator to automatically validate character limits on request data.
    
    This decorator checks JSON request data for item_name and borrower_name fields
    and validates their character limits before calling the decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.is_json:
            data = request.get_json()
            is_valid, errors = validate_character_limits(data)
            
            if not is_valid:
                return jsonify({
                    'error': 'Validation failed',
                    'details': errors
                }), 400
        
        return f(*args, **kwargs)
    
    return decorated_function


# Error handler for ValidationError
@blueprint.errorhandler(ValidationError)
def handle_validation_error(error):
    """Handle ValidationError exceptions."""
    response = {
        'error': 'Validation error',
        'message': error.message
    }
    if error.field:
        response['field'] = error.field
    
    return jsonify(response), 400
