"""Retain generated routes while sharing one safe store."""
from flask import Blueprint
from backend.core.loans import records_response

blueprint = Blueprint('capability_record_item_and_borrower_3af7a315', __name__)

@blueprint.post('/api/capability_record_item_and_borrower_3af7a315/loan-records')
def create_loan_record():
    return records_response()

@blueprint.get('/api/capability_record_item_and_borrower_3af7a315/loan-records')
def get_loan_records():
    return records_response('loan_records')
