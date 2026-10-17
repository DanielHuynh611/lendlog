"""Read the canonical store rather than an unrelated generated table."""
from flask import Blueprint
from backend.core.loans import records_response

blueprint = Blueprint('capability_view_loan_list_e3bf329c', __name__)

@blueprint.get('/api/capability_view_loan_list_e3bf329c/loans')
def get_loans():
    return records_response()
