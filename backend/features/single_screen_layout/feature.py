"""Single screen layout feature module.

This module provides a single screen layout displaying form fields and loan list
with the form above the list.
"""

from flask import Blueprint, render_template, jsonify, request
from functools import wraps
import logging

logger = logging.getLogger(__name__)

blueprint = Blueprint('single_screen_layout', __name__, url_prefix='/single-screen-layout')


def handle_errors(f):
    """Decorator to handle errors in route handlers."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Validation error in {f.__name__}: {str(e)}")
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return decorated_function


@blueprint.route('/layout', methods=['GET'])
@handle_errors
def get_single_screen_layout():
    """Get the single screen layout configuration.
    
    Returns layout configuration for displaying form fields above loan list.
    """
    layout_config = {
        'layout_type': 'single_screen',
        'sections': [
            {
                'id': 'form_section',
                'type': 'form',
                'position': 'top',
                'order': 1
            },
            {
                'id': 'list_section',
                'type': 'list',
                'position': 'bottom',
                'order': 2
            }
        ],
        'display_mode': 'stacked'
    }
    return jsonify(layout_config), 200


@blueprint.route('/layout/config', methods=['POST'])
@handle_errors
def update_layout_config():
    """Update layout configuration.
    
    Accepts layout preferences and returns updated configuration.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate layout configuration
    layout_type = data.get('layout_type', 'single_screen')
    display_mode = data.get('display_mode', 'stacked')
    
    if layout_type not in ['single_screen', 'split_screen', 'tabbed']:
        return jsonify({'error': 'Invalid layout type'}), 400
    
    if display_mode not in ['stacked', 'side_by_side', 'overlay']:
        return jsonify({'error': 'Invalid display mode'}), 400
    
    response = {
        'success': True,
        'layout_type': layout_type,
        'display_mode': display_mode,
        'message': 'Layout configuration updated successfully'
    }
    
    return jsonify(response), 200


@blueprint.route('/layout/sections', methods=['GET'])
@handle_errors
def get_layout_sections():
    """Get available layout sections.
    
    Returns information about form and list sections.
    """
    sections = {
        'form_section': {
            'id': 'form_section',
            'title': 'Loan Application Form',
            'description': 'Form fields for creating or editing loan applications',
            'position': 'top',
            'visible': True,
            'collapsible': False
        },
        'list_section': {
            'id': 'list_section',
            'title': 'Loan List',
            'description': 'List of all loan applications',
            'position': 'bottom',
            'visible': True,
            'collapsible': True
        }
    }
    
    return jsonify(sections), 200


@blueprint.route('/layout/preferences', methods=['GET'])
@handle_errors
def get_layout_preferences():
    """Get user layout preferences.
    
    Returns current user preferences for the single screen layout.
    """
    preferences = {
        'form_expanded': True,
        'list_expanded': True,
        'form_height': 'auto',
        'list_height': 'auto',
        'spacing': 'medium',
        'theme': 'default'
    }
    
    return jsonify(preferences), 200


@blueprint.route('/layout/preferences', methods=['PUT'])
@handle_errors
def update_layout_preferences():
    """Update user layout preferences.
    
    Accepts and stores user preferences for the single screen layout.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No preferences provided'}), 400
    
    # Validate preferences
    valid_spacing = ['compact', 'medium', 'comfortable']
    valid_themes = ['default', 'dark', 'light', 'high_contrast']
    
    spacing = data.get('spacing', 'medium')
    theme = data.get('theme', 'default')
    
    if spacing not in valid_spacing:
        return jsonify({'error': 'Invalid spacing value'}), 400
    
    if theme not in valid_themes:
        return jsonify({'error': 'Invalid theme value'}), 400
    
    response = {
        'success': True,
        'preferences': {
            'form_expanded': data.get('form_expanded', True),
            'list_expanded': data.get('list_expanded', True),
            'form_height': data.get('form_height', 'auto'),
            'list_height': data.get('list_height', 'auto'),
            'spacing': spacing,
            'theme': theme
        },
        'message': 'Preferences updated successfully'
    }
    
    return jsonify(response), 200


@blueprint.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the single screen layout feature."""
    return jsonify({
        'status': 'healthy',
        'feature': 'single_screen_layout',
        'version': '1.0.0'
    }), 200
