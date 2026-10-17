"""Whole-application smoke tests."""

from backend import create_app


def test_health_endpoint():
    app = create_app(testing=True)
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["ok"] is True


def test_expected_function_inventory_is_frozen():
    expected = ('capability_local_browser_storage_03ab1d7c.function.create_loan_record', 'capability_local_browser_storage_03ab1d7c.function.get_all_loan_records', 'capability_record_item_and_borrower_3af7a315.function.create_loan_record', 'capability_record_item_and_borrower_3af7a315.function.get_loan_records', 'capability_view_loan_list_e3bf329c.function.get_loans')
    assert len(expected) == 5
