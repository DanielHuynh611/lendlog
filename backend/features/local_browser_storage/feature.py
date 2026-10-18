"""Retain generated route names while using a browser-isolated API store."""
from flask import Blueprint
from backend.core.loans import records_response

blueprint = Blueprint('capability_local_browser_storage_03ab1d7c', __name__)

@blueprint.post('/api/capability_local_browser_storage_03ab1d7c/loans')
@blueprint.post('/api/loans')
def create_loan_record():
    return records_response()

@blueprint.get('/api/capability_local_browser_storage_03ab1d7c/loans')
@blueprint.get('/api/loans')
def get_all_loan_records():
    return records_response()


@blueprint.post('/api/loans/<loan_id>/return')
def mark_returned(loan_id):
    from backend.core.loans import return_response
    return return_response(loan_id)


@blueprint.post('/api/loans/<loan_id>/restore')
def mark_outstanding(loan_id):
    from backend.core.loans import restore_response
    return restore_response(loan_id)


@blueprint.patch('/api/loans/<loan_id>')
def edit_loan(loan_id):
    from backend.core.loans import edit_response
    return edit_response(loan_id)


@blueprint.delete('/api/loans/<loan_id>')
def delete_loan(loan_id):
    from backend.core.loans import delete_response
    return delete_response(loan_id)
