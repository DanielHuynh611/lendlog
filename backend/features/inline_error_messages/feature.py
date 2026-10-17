"""
Inline error messages module for Flask application.

This module provides utilities for generating and formatting inline validation
error messages that can be displayed in forms and API responses.
"""

from flask import Blueprint, jsonify, request
from functools import wraps
from typing import Dict, List, Any, Callable
import re


blueprint = Blueprint('inline_error_messages', __name__)


class ValidationError(Exception):
    """Custom exception for validation errors with field-specific messages."""
    
    def __init__(self, errors: Dict[str, str]):
        """
        Initialize validation error with field-specific error messages.
        
        Args:
            errors: Dictionary mapping field names to error messages
        """
        self.errors = errors
        super().__init__("Validation failed")


class FieldValidator:
    """Validator class for common field validation rules."""
    
    @staticmethod
    def required(value: Any, field_name: str) -> str:
        """Validate that a field is not empty."""
        if value is None or (isinstance(value, str) and not value.strip()):
            return f"{field_name} is required"
        return ""
    
    @staticmethod
    def email(value: str, field_name: str) -> str:
        """Validate email format."""
        if not value:
            return ""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            return f"{field_name} must be a valid email address"
        return ""
    
    @staticmethod
    def min_length(value: str, min_len: int, field_name: str) -> str:
        """Validate minimum string length."""
        if value and len(value) < min_len:
            return f"{field_name} must be at least {min_len} characters"
        return ""
    
    @staticmethod
    def max_length(value: str, max_len: int, field_name: str) -> str:
        """Validate maximum string length."""
        if value and len(value) > max_len:
            return f"{field_name} must not exceed {max_len} characters"
        return ""
    
    @staticmethod
    def numeric(value: Any, field_name: str) -> str:
        """Validate that value is numeric."""
        if value is None or value == "":
            return ""
        try:
            float(value)
            return ""
        except (ValueError, TypeError):
            return f"{field_name} must be a number"
    
    @staticmethod
    def min_value(value: Any, min_val: float, field_name: str) -> str:
        """Validate minimum numeric value."""
        if value is None or value == "":
            return ""
        try:
            if float(value) < min_val:
                return f"{field_name} must be at least {min_val}"
        except (ValueError, TypeError):
            pass
        return ""
    
    @staticmethod
    def max_value(value: Any, max_val: float, field_name: str) -> str:
        """Validate maximum numeric value."""
        if value is None or value == "":
            return ""
        try:
            if float(value) > max_val:
                return f"{field_name} must not exceed {max_val}"
        except (ValueError, TypeError):
            pass
        return ""
    
    @staticmethod
    def pattern(value: str, pattern: str, field_name: str, message: str = None) -> str:
        """Validate value against regex pattern."""
        if not value:
            return ""
        if not re.match(pattern, value):
            return message or f"{field_name} format is invalid"
        return ""


def validate_fields(validation_rules: Dict[str, List[Callable]]) -> Callable:
    """
    Decorator to validate request data against specified rules.
    
    Args:
        validation_rules: Dictionary mapping field names to lists of validation functions
    
    Returns:
        Decorated function that performs validation before execution
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json() if request.is_json else request.form.to_dict()
            errors = {}
            
            for field_name, validators in validation_rules.items():
                field_value = data.get(field_name)
                for validator in validators:
                    error_msg = validator(field_value)
                    if error_msg:
                        errors[field_name] = error_msg
                        break  # Stop at first error for this field
            
            if errors:
                raise ValidationError(errors)
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def format_error_response(errors: Dict[str, str], status_code: int = 400) -> tuple:
    """
    Format validation errors into a standardized JSON response.
    
    Args:
        errors: Dictionary of field names to error messages
        status_code: HTTP status code for the response
    
    Returns:
        Tuple of (response, status_code)
    """
    return jsonify({
        'success': False,
        'errors': errors,
        'message': 'Validation failed'
    }), status_code


def format_single_error(field: str, message: str, status_code: int = 400) -> tuple:
    """
    Format a single field error into a JSON response.
    
    Args:
        field: Field name that failed validation
        message: Error message
        status_code: HTTP status code for the response
    
    Returns:
        Tuple of (response, status_code)
    """
    return format_error_response({field: message}, status_code)


@blueprint.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    """Global error handler for ValidationError exceptions."""
    return format_error_response(error.errors, 400)


@blueprint.app_errorhandler(ValidationError)
def handle_app_validation_error(error: ValidationError):
    """Application-wide error handler for ValidationError exceptions."""
    return format_error_response(error.errors, 400)


def get_field_errors(data: Dict[str, Any], rules: Dict[str, List[tuple]]) -> Dict[str, str]:
    """
    Validate data against rules and return field-specific errors.
    
    Args:
        data: Dictionary of field values to validate
        rules: Dictionary mapping field names to lists of (validator_func, *args) tuples
    
    Returns:
        Dictionary of field names to error messages
    """
    errors = {}
    
    for field_name, field_rules in rules.items():
        field_value = data.get(field_name)
        for rule in field_rules:
            if callable(rule):
                error_msg = rule(field_value)
            elif isinstance(rule, tuple) and len(rule) > 0:
                validator_func = rule[0]
                args = rule[1:]
                error_msg = validator_func(field_value, *args)
            else:
                continue
            
            if error_msg:
                errors[field_name] = error_msg
                break  # Only show first error per field
    
    return errors


def create_validator(field_name: str, **rules) -> Callable:
    """
    Create a validator function for a specific field with given rules.
    
    Args:
        field_name: Name of the field to validate
        **rules: Validation rules (required, email, min_length, max_length, etc.)
    
    Returns:
        Validator function that returns error message or empty string
    """
    def validator(value: Any) -> str:
        if rules.get('required') and not value:
            return f"{field_name} is required"
        
        if not value:
            return ""
        
        if rules.get('email'):
            error = FieldValidator.email(value, field_name)
            if error:
                return error
        
        if 'min_length' in rules:
            error = FieldValidator.min_length(value, rules['min_length'], field_name)
            if error:
                return error
        
        if 'max_length' in rules:
            error = FieldValidator.max_length(value, rules['max_length'], field_name)
            if error:
                return error
        
        if rules.get('numeric'):
            error = FieldValidator.numeric(value, field_name)
            if error:
                return error
        
        if 'min_value' in rules:
            error = FieldValidator.min_value(value, rules['min_value'], field_name)
            if error:
                return error
        
        if 'max_value' in rules:
            error = FieldValidator.max_value(value, rules['max_value'], field_name)
            if error:
                return error
        
        if 'pattern' in rules:
            pattern = rules['pattern']
            message = rules.get('pattern_message')
            error = FieldValidator.pattern(value, pattern, field_name, message)
            if error:
                return error
        
        return ""
    
    return validator


# Utility functions for common validation scenarios
def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, str]:
    """
    Validate that all required fields are present and non-empty.
    
    Args:
        data: Dictionary of field values
        required_fields: List of required field names
    
    Returns:
        Dictionary of field names to error messages
    """
    errors = {}
    for field in required_fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors[field] = f"{field.replace('_', ' ').title()} is required"
    return errors


def validate_email_field(email: str, field_name: str = "Email") -> str:
    """
    Validate email format and return error message if invalid.
    
    Args:
        email: Email address to validate
        field_name: Display name for the field
    
    Returns:
        Error message or empty string if valid
    """
    return FieldValidator.email(email, field_name)


def validate_password_strength(password: str, min_length: int = 8) -> str:
    """
    Validate password strength requirements.
    
    Args:
        password: Password to validate
        min_length: Minimum required length
    
    Returns:
        Error message or empty string if valid
    """
    if not password:
        return "Password is required"
    
    if len(password) < min_length:
        return f"Password must be at least {min_length} characters"
    
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one number"
    
    return ""


# Export public API
__all__ = [
    'blueprint',
    'ValidationError',
    'FieldValidator',
    'validate_fields',
    'format_error_response',
    'format_single_error',
    'get_field_errors',
    'create_validator',
    'validate_required_fields',
    'validate_email_field',
    'validate_password_strength'
]
