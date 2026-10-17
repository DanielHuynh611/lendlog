# Full-stack verification

These checks use a temporary directory and verification configuration, not your deployment. The smoke command requests registered pages and JavaScript assets; it does not exercise form submissions or database business operations.

## Findings and next steps
No issues were recorded by these checks. This does not cover checks that were not run.

## Static assembly evidence
```json
{
  "application_contract_version": "frontend-experience-1",
  "application_contract_hash": "7eb33ffec2fac45055e547d6dffd3c70f5e48a743124c84e611c4fc8d0180c59",
  "screen_contracts_valid": true,
  "declared_interactions_valid": false,
  "static_screen_ids": [
    "capability_character_limit_validation_533aef43.screen.main_loan_entry",
    "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors",
    "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
    "capability_record_item_and_borrower_3af7a315.screen.loan_entry",
    "capability_required_field_validation_18c05c66.screen.loan_entry_form",
    "capability_single_screen_layout_3203f8ec.screen.main",
    "capability_view_loan_list_e3bf329c.screen.loan_list"
  ],
  "non_blocking_errors": [
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_record_item_and_borrower_3af7a315.screen.loan_entry",
      "unregistered_path": "frontend/features/record_item_and_borrower/loan_entry_screen.html",
      "code": "frontend_screen_route_collision",
      "message": "Completed pages share this route. The registered page is served; the other page remains in the package at its recorded path.",
      "repair": "Assign a unique route to the unregistered page in fullstack.py, update its links, and repeat the route check."
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_view_loan_list_e3bf329c.screen.loan_list",
      "unregistered_path": "frontend/features/view_loan_list/loan_list.html",
      "code": "frontend_screen_route_collision",
      "message": "Completed pages share this route. The registered page is served; the other page remains in the package at its recorded path.",
      "repair": "Assign a unique route to the unregistered page in fullstack.py, update its links, and repeat the route check."
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_character_limit_validation_533aef43.screen.main_loan_entry",
      "unregistered_path": "frontend/features/character_limit_validation/main_loan_entry_screen.html",
      "code": "frontend_screen_route_collision",
      "message": "Completed pages share this route. The registered page is served; the other page remains in the package at its recorded path.",
      "repair": "Assign a unique route to the unregistered page in fullstack.py, update its links, and repeat the route check."
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_required_field_validation_18c05c66.screen.loan_entry_form",
      "unregistered_path": "frontend/features/required_field_validation/loan_entry_form_with_validation.html",
      "code": "frontend_screen_route_collision",
      "message": "Completed pages share this route. The registered page is served; the other page remains in the package at its recorded path.",
      "repair": "Assign a unique route to the unregistered page in fullstack.py, update its links, and repeat the route check."
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_single_screen_layout_3203f8ec.screen.main",
      "unregistered_path": "frontend/features/single_screen_layout/main_screen.html",
      "code": "frontend_screen_route_collision",
      "message": "Completed pages share this route. The registered page is served; the other page remains in the package at its recorded path.",
      "repair": "Assign a unique route to the unregistered page in fullstack.py, update its links, and repeat the route check."
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors",
      "unregistered_path": "frontend/features/inline_error_messages/main_form_with_inline_error_messages.html",
      "code": "frontend_screen_route_collision",
      "message": "Completed pages share this route. The registered page is served; the other page remains in the package at its recorded path.",
      "repair": "Assign a unique route to the unregistered page in fullstack.py, update its links, and repeat the route check."
    }
  ],
  "journeys_verified": false,
  "verification_level": "contracts_and_page_serving",
  "static_valid": true,
  "backend_package_reused_unchanged": true,
  "backend_application_import_normalized_paths": [],
  "route_collisions_absent": false,
  "route_collisions": [
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_record_item_and_borrower_3af7a315.screen.loan_entry",
      "unregistered_path": "frontend/features/record_item_and_borrower/loan_entry_screen.html"
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_view_loan_list_e3bf329c.screen.loan_list",
      "unregistered_path": "frontend/features/view_loan_list/loan_list.html"
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_character_limit_validation_533aef43.screen.main_loan_entry",
      "unregistered_path": "frontend/features/character_limit_validation/main_loan_entry_screen.html"
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_required_field_validation_18c05c66.screen.loan_entry_form",
      "unregistered_path": "frontend/features/required_field_validation/loan_entry_form_with_validation.html"
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_single_screen_layout_3203f8ec.screen.main",
      "unregistered_path": "frontend/features/single_screen_layout/main_screen.html"
    },
    {
      "route": "/",
      "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
      "unregistered_screen_id": "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors",
      "unregistered_path": "frontend/features/inline_error_messages/main_form_with_inline_error_messages.html"
    }
  ],
  "screen_files_present": true,
  "self_contained_frontend": true,
  "legacy_runtime_normalized_paths": [],
  "source_snapshot_hash": "d0d47c59b64ec86790ad41e1630130dfb4e6897efa4d7b3cb04f8f98a79df6de",
  "errors": []
}
```

## Routes needing attention
The first page registered at a URL is served; additional pages remain in the ZIP. Choose unique routes for the unregistered paths in `fullstack.py`, update page links and rerun the route smoke check.
```json
[
  {
    "route": "/",
    "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
    "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
    "unregistered_screen_id": "capability_record_item_and_borrower_3af7a315.screen.loan_entry",
    "unregistered_path": "frontend/features/record_item_and_borrower/loan_entry_screen.html"
  },
  {
    "route": "/",
    "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
    "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
    "unregistered_screen_id": "capability_view_loan_list_e3bf329c.screen.loan_list",
    "unregistered_path": "frontend/features/view_loan_list/loan_list.html"
  },
  {
    "route": "/",
    "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
    "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
    "unregistered_screen_id": "capability_character_limit_validation_533aef43.screen.main_loan_entry",
    "unregistered_path": "frontend/features/character_limit_validation/main_loan_entry_screen.html"
  },
  {
    "route": "/",
    "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
    "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
    "unregistered_screen_id": "capability_required_field_validation_18c05c66.screen.loan_entry_form",
    "unregistered_path": "frontend/features/required_field_validation/loan_entry_form_with_validation.html"
  },
  {
    "route": "/",
    "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
    "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
    "unregistered_screen_id": "capability_single_screen_layout_3203f8ec.screen.main",
    "unregistered_path": "frontend/features/single_screen_layout/main_screen.html"
  },
  {
    "route": "/",
    "registered_screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
    "registered_path": "frontend/features/local_browser_storage/main_loan_list.html",
    "unregistered_screen_id": "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors",
    "unregistered_path": "frontend/features/inline_error_messages/main_form_with_inline_error_messages.html"
  }
]
```

## Runtime commands and captured results
```json
{
  "valid": true,
  "passes": {
    "compile": true,
    "application_start": true,
    "screen_routes": true,
    "self_contained_frontend": true,
    "frontend_assets": true
  },
  "commands": [
    {
      "command": [
        "/home/ubuntu/zorentia-app/venv/bin/python",
        "-m",
        "compileall",
        "-q",
        "backend",
        "frontend",
        "fullstack.py"
      ],
      "returncode": 0,
      "stdout": "",
      "stderr": "",
      "timed_out": false
    },
    {
      "command": [
        "/home/ubuntu/zorentia-app/venv/bin/python",
        "-c",
        "from fullstack import create_app;app=create_app(testing=True);client=app.test_client();routes=['/'];responses=[client.get(route) for route in routes];print({'route_checks':[{'route':route,'status':response.status_code,'html_doctype':b'<!doctype html' in response.data.lower(),'compiler_marker':b'data-zorentia-compiler' in response.data} for route,response in zip(routes,responses)]},flush=True);assert responses and all(response.status_code==200 for response in responses);assert all(b'<!doctype html' in response.data.lower() for response in responses);assert all(b'data-zorentia-compiler' in response.data for response in responses);assets=['/__frontend_assets/frontend/shared/ui/library.js', '/__frontend_assets/frontend/shared/ui/runtime.js', '/__frontend_assets/frontend/features/local_browser_storage/main_loan_list.js', '/__frontend_assets/frontend/features/record_item_and_borrower/loan_entry_screen.js', '/__frontend_assets/frontend/features/view_loan_list/loan_list.js', '/__frontend_assets/frontend/features/character_limit_validation/main_loan_entry_screen.js', '/__frontend_assets/frontend/features/required_field_validation/loan_entry_form_with_validation.js', '/__frontend_assets/frontend/features/single_screen_layout/main_screen.js', '/__frontend_assets/frontend/features/inline_error_messages/main_form_with_inline_error_messages.js'];asset_responses=[client.get(asset) for asset in assets];print({'asset_checks':[{'path':asset,'status':response.status_code,'content_type':response.content_type} for asset,response in zip(assets,asset_responses)]},flush=True);assert all(response.status_code==200 for response in asset_responses);assert all('javascript' in response.content_type for response in asset_responses);print({'routes':[(route,response.status_code) for route,response in zip(routes,responses)],'assets':[(asset,response.status_code) for asset,response in zip(assets,asset_responses)]})"
      ],
      "returncode": 0,
      "stdout": "{'route_checks': [{'route': '/', 'status': 200, 'html_doctype': True, 'compiler_marker': True}]}\n{'asset_checks': [{'path': '/__frontend_assets/frontend/shared/ui/library.js', 'status': 200, 'content_type': 'text/javascript; charset=utf-8'}, {'path': '/__frontend_assets/frontend/shared/ui/runtime.js', 'status': 200, 'content_type': 'text/javascript; charset=utf-8'}, {'path': '/__frontend_assets/frontend/features/local_browser_storage/main_loan_list.js', 'status': 200, 'content_type': 'text/javascript; charset=utf-8'}, {'path': '/__frontend_assets/frontend/features/record_item_and_borrower/loan_entry_screen.js', 'status': 200, 'content_type': 'text/javascript; charset=utf-8'}, {'path': '/__frontend_assets/frontend/features/view_loan_list/loan_list.js', 'status': 200, 'content_type': 'text/javascript; charset=utf-8'}, {'path': '/__frontend_assets/frontend/features/character_limit_validation/main_loan_entry_screen.js', 'status': 200, 'content_type': 'text/javascript; charset=utf-8'}, {'path': '/__frontend_assets/frontend/features/required_field_validation/loan_entry_form_with_validation.js', 'status': 200, 'content_type': 'text/javascript; charset=utf-8'}, {'path': '/__frontend_assets/frontend/features/single_screen_layout/main_screen.js', 'status': 200, 'content_type': 'text/javascript; charset=utf-8'}, {'path': '/__frontend_assets/frontend/features/inline_error_messages/main_form_with_inline_error_messages.js', 'status': 200, 'content_type': 'text/javascript; charset=utf-8'}]}\n{'routes': [('/', 200)], 'assets': [('/__frontend_assets/frontend/shared/ui/library.js', 200), ('/__frontend_assets/frontend/shared/ui/runtime.js', 200), ('/__frontend_assets/frontend/features/local_browser_storage/main_loan_list.js', 200), ('/__frontend_assets/frontend/features/record_item_and_borrower/loan_entry_screen.js', 200), ('/__frontend_assets/frontend/features/view_loan_list/loan_list.js', 200), ('/__frontend_assets/frontend/features/character_limit_validation/main_loan_entry_screen.js', 200), ('/__frontend_assets/frontend/features/required_field_validation/loan_entry_form_with_validation.js', 200), ('/__frontend_assets/frontend/features/single_screen_layout/main_screen.js', 200), ('/__frontend_assets/frontend/features/inline_error_messages/main_form_with_inline_error_messages.js', 200)]}\n",
      "stderr": "",
      "timed_out": false
    }
  ],
  "errors": [],
  "execution_scope": {
    "compile": "executed",
    "application_start_and_route_asset_smoke": "executed",
    "not_run": [
      "MySQL schema execution",
      "pytest",
      "browser interaction",
      "end-to-end business behavior",
      "deployment verification"
    ],
    "output_limit": "Each command retains the last 8000 characters of stdout/stderr; earlier output may be unavailable."
  }
}
```

Reproduce a failure using the recorded command from the package root after following README-FULLSTACK.md. For the smoke command, use your environment's Python executable. Compare the traceback, file/line and exit code; a timeout does not establish a code defect.
