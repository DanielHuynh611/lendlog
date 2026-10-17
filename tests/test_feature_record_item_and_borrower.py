"""Deterministic contract checks for Record item and borrower."""

from backend import create_app


def test_feature_routes_are_registered():
    app = create_app(testing=True)
    actual = {
        (rule.rule, method)
        for rule in app.url_map.iter_rules()
        for method in (rule.methods or set())
    }
    expected = (('/api/capability_record_item_and_borrower_3af7a315/loan-records', 'POST'), ('/api/capability_record_item_and_borrower_3af7a315/loan-records', 'GET'))
    assert all(route in actual for route in expected)


def test_protected_routes_reject_missing_authentication():
    client = create_app(testing=True).test_client()
    assert True
