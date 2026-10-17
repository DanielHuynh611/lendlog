"""Retain generated route names while using a browser-isolated API store."""
from flask import Blueprint
from backend.core.loans import records_response

blueprint = Blueprint('capability_local_browser_storage_03ab1d7c', __name__)

@blueprint.post('/api/capability_local_browser_storage_03ab1d7c/loans')
def create_loan_record():
    return records_response()

@blueprint.get('/api/capability_local_browser_storage_03ab1d7c/loans')
def get_all_loan_records():
    return records_response()
