# Backend verification

Static checks inspect Python syntax, internal import paths, declared routes/functions, file integrity and credential patterns. `database_contract` means the schema file exists; `dependency_resolution` means requirements.txt exists, not that installation succeeded. `file_integrity` is the verifier's aggregate static result. The raw evidence identifies individual errors. The checked-input package hash below covers the files before reports were added.

## Findings and next steps
No issues were recorded by these checks. This does not cover checks that were not run.

## Check evidence and coverage
```json
{
  "schema_version": "assembled-backend-verification",
  "source": {
    "architecture_session_id": "631fd820-3732-40c0-a3e6-1dd2d9e88022",
    "architecture_id": "architecture:scope_lendlog_bdfde953:9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604",
    "architecture_source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604"
  },
  "package_hash": "39df47d30d39f485127b70944849d9d815f2015498d6628d8a9cbef391af25e0",
  "static_valid": true,
  "passes": {
    "file_integrity": true,
    "imports": true,
    "route_map": true,
    "function_coverage": true,
    "database_contract": true,
    "dependency_resolution": true,
    "secret_scan": "[redacted]"
  },
  "features": {
    "covered": 7,
    "total": 7
  },
  "functions": {
    "covered": 5,
    "total": 5
  },
  "errors": [],
  "warnings": [],
  "non_blocking_errors": [],
  "report_hash": "d18ee28139f4963136f189f1df5de3135c81164d3b7e560ec5fbc0db13daa53b",
  "database_contract_repair": {
    "paths": [
      "backend/features/record_item_and_borrower/feature.py"
    ],
    "platform_normalizations": [],
    "runtime": {
      "valid": true,
      "failure_kind": null,
      "passes": {
        "disposable_mysql": true,
        "compile": true,
        "application_start": true,
        "feature_tests": true,
        "integration_tests": false,
        "contract_smoke_tests": true
      },
      "mysql_version": "8.0.45",
      "commands": [
        {
          "command": [
            "/home/ubuntu/zorentia-app/venv/bin/python",
            "-m",
            "compileall",
            "-q",
            "backend",
            "tests"
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
            "from backend import create_app;app=create_app(testing=True);client=app.test_client();response=client.get('/health');assert response.status_code==200;print(sorted((r.rule,','.join(sorted(r.methods or []))) for r in app.url_map.iter_rules()))"
          ],
          "returncode": 0,
          "stdout": "[('/api/capability_local_browser_storage_03ab1d7c/loans', 'GET,HEAD,OPTIONS'), ('/api/capability_local_browser_storage_03ab1d7c/loans', 'OPTIONS,POST'), ('/api/capability_record_item_and_borrower_3af7a315/loan-records', 'GET,HEAD,OPTIONS'), ('/api/capability_record_item_and_borrower_3af7a315/loan-records', 'OPTIONS,POST'), ('/api/capability_view_loan_list_e3bf329c/loans', 'GET,HEAD,OPTIONS'), ('/health', 'GET,HEAD,OPTIONS'), ('/static/<path:filename>', 'GET,HEAD,OPTIONS')]\n",
          "stderr": "",
          "timed_out": false
        },
        {
          "command": [
            "/home/ubuntu/zorentia-app/venv/bin/python",
            "-m",
            "pytest",
            "-q",
            "--disable-warnings"
          ],
          "returncode": 0,
          "stdout": "................                                                         [100%]\n16 passed in 0.43s\n",
          "stderr": "",
          "timed_out": false
        }
      ],
      "errors": []
    },
    "backup_version_id": "01050816-1908-4ee6-9044-c063e8e577f2"
  },
  "not_run": [
    "database execution",
    "dependency installation",
    "application startup",
    "pytest",
    "integration tests",
    "business behavior"
  ]
}
```

## Feature sources
```json
[
  {
    "feature_id": "capability_local_browser_storage_03ab1d7c",
    "state": "complete",
    "architecture_backend_hash": "e43c8da2634fa554dbefaa8ee7f4e746811398dcd41d11e7c1f8ddcd94898b82",
    "database_feature_sql_hash": "3d2b1942db323dc1a58470d44a2cee29201d00d60843b3e5ccf63ab74dbae510",
    "last_error_code": null,
    "last_error_details": []
  },
  {
    "feature_id": "capability_record_item_and_borrower_3af7a315",
    "state": "complete",
    "architecture_backend_hash": "f5bb3a07d15cbae76be20c15c4d57f239863d33b1d0693b71fe9e7598442270d",
    "database_feature_sql_hash": "a9d0d5cf6d37a2d8838d6a162027ebf4392b0d35c71572bd912f127f3d9682d3",
    "last_error_code": null,
    "last_error_details": []
  },
  {
    "feature_id": "capability_view_loan_list_e3bf329c",
    "state": "complete",
    "architecture_backend_hash": "66a14995095325e435f358178b6431518e8a0fcb363fa8d8a0a4f45e27992824",
    "database_feature_sql_hash": "5bb71981b69e4d6dbd7baff687099bc0c2ae7ac2cf9d73a5c2f54f30361a7252",
    "last_error_code": null,
    "last_error_details": []
  },
  {
    "feature_id": "capability_character_limit_validation_533aef43",
    "state": "complete",
    "architecture_backend_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "database_feature_sql_hash": "9d851035071f18daebefdf2c894be63680e1db252013dea94c7eaed76e109616",
    "last_error_code": null,
    "last_error_details": []
  },
  {
    "feature_id": "capability_required_field_validation_18c05c66",
    "state": "complete",
    "architecture_backend_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "database_feature_sql_hash": "dc438b2ed3103715511021f9fba2b51f56365113cf9b858bffee30371459fe04",
    "last_error_code": null,
    "last_error_details": []
  },
  {
    "feature_id": "capability_single_screen_layout_3203f8ec",
    "state": "complete",
    "architecture_backend_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "database_feature_sql_hash": "ff2501f9eea3bcb0b3e9630509374a2c0ec261bae07d5cf0dda2e0235f934bea",
    "last_error_code": null,
    "last_error_details": []
  },
  {
    "feature_id": "capability_inline_error_messages_9ddfedf0",
    "state": "complete",
    "architecture_backend_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "database_feature_sql_hash": "66c535ace49f2ee734f9b288cafc87675d134bc78717748d33c879619d94d38a",
    "last_error_code": null,
    "last_error_details": []
  }
]
```

## Expected feature routes and functions
```json
[
  {
    "feature_id": "capability_local_browser_storage_03ab1d7c",
    "functions": [
      {
        "id": "capability_local_browser_storage_03ab1d7c.function.create_loan_record",
        "name": "create_loan_record",
        "http_method": "POST",
        "route": "/api/capability_local_browser_storage_03ab1d7c/loans",
        "trigger_type": "user_action"
      },
      {
        "id": "capability_local_browser_storage_03ab1d7c.function.get_all_loan_records",
        "name": "get_all_loan_records",
        "http_method": "GET",
        "route": "/api/capability_local_browser_storage_03ab1d7c/loans",
        "trigger_type": "user_action"
      }
    ]
  },
  {
    "feature_id": "capability_record_item_and_borrower_3af7a315",
    "functions": [
      {
        "id": "capability_record_item_and_borrower_3af7a315.function.create_loan_record",
        "name": "create_loan_record",
        "http_method": "POST",
        "route": "/api/capability_record_item_and_borrower_3af7a315/loan-records",
        "trigger_type": "user_action"
      },
      {
        "id": "capability_record_item_and_borrower_3af7a315.function.get_loan_records",
        "name": "get_loan_records",
        "http_method": "GET",
        "route": "/api/capability_record_item_and_borrower_3af7a315/loan-records",
        "trigger_type": "user_action"
      }
    ]
  },
  {
    "feature_id": "capability_view_loan_list_e3bf329c",
    "functions": [
      {
        "id": "capability_view_loan_list_e3bf329c.function.get_loans",
        "name": "get_loans",
        "http_method": "GET",
        "route": "/api/capability_view_loan_list_e3bf329c/loans",
        "trigger_type": "user_action"
      }
    ]
  },
  {
    "feature_id": "capability_character_limit_validation_533aef43",
    "functions": []
  },
  {
    "feature_id": "capability_required_field_validation_18c05c66",
    "functions": []
  },
  {
    "feature_id": "capability_single_screen_layout_3203f8ec",
    "functions": []
  },
  {
    "feature_id": "capability_inline_error_messages_9ddfedf0",
    "functions": []
  }
]
```

## Generation and repair history

Failed attempts below are historical, not automatically defects in these files. A matching file hash identifies a checked output retained in this package. Earlier discarded evidence cannot be reconstructed. An empty history does not mean every attempt passed.

### Checked output matches packaged files

```json
{
  "stage": "backend feature",
  "feature": "capability_local_browser_storage_03ab1d7c",
  "screen": null,
  "outcome": "completed"
}
```

```json
{
  "stage": "backend feature",
  "tool_slug": "backend-generator",
  "checks": [
    {
      "check": "Backend syntax, functions and routes",
      "status": "passed",
      "files": [
        {
          "path": "backend/features/local_browser_storage/feature.py",
          "sha256": "0772bc2466f1f3320adb6f5e28794011acd7fa2237df2dc7c58aa60ecf13d17c"
        }
      ],
      "result": {
        "valid": true,
        "feature_id": "capability_local_browser_storage_03ab1d7c",
        "file_count": 1,
        "function_ids": [
          "capability_local_browser_storage_03ab1d7c.function.create_loan_record",
          "capability_local_browser_storage_03ab1d7c.function.get_all_loan_records"
        ],
        "function_names": [
          "create_loan_record",
          "get_all_loan_records"
        ],
        "route_count": 2,
        "verification_hash": "6b5d1d86b82ba7af3ab3374d375d1751d336e8c0d6686dc5cb4d201af88c2c88"
      }
    }
  ],
  "started_at": "2026-10-14T12:18:48.647489+00:00",
  "workspace_id": "007518e7-2462-43d5-9206-ad0a779472c6",
  "feature_id": "capability_local_browser_storage_03ab1d7c",
  "screen_id": null,
  "expected_workspace_version": 1,
  "session_id": "50237586-586f-424b-b23b-e6a24c7f6b29",
  "mvp_session_id": "45526ed8-d80d-44c2-b25d-6440dc4ff343",
  "source": {
    "architecture_backend_hash": "e43c8da2634fa554dbefaa8ee7f4e746811398dcd41d11e7c1f8ddcd94898b82",
    "database_feature_sql_hash": "3d2b1942db323dc1a58470d44a2cee29201d00d60843b3e5ccf63ab74dbae510"
  },
  "outcome": "completed",
  "finished_at": "2026-10-14T12:19:01.182838+00:00"
}
```

### Historical attempt; not evidence of a current defect

```json
{
  "stage": "backend feature",
  "feature": "capability_record_item_and_borrower_3af7a315",
  "screen": null,
  "outcome": "completed"
}
```

```json
{
  "stage": "backend feature",
  "tool_slug": "backend-generator",
  "checks": [
    {
      "check": "Backend syntax, functions and routes",
      "status": "passed",
      "files": [
        {
          "path": "backend/features/record_item_and_borrower/feature.py",
          "sha256": "b981968e0fb04de72aebf6047182345ecf25d2e322e07d2bed9d8d8baf1b59ba"
        }
      ],
      "result": {
        "valid": true,
        "feature_id": "capability_record_item_and_borrower_3af7a315",
        "file_count": 1,
        "function_ids": [
          "capability_record_item_and_borrower_3af7a315.function.create_loan_record",
          "capability_record_item_and_borrower_3af7a315.function.get_loan_records"
        ],
        "function_names": [
          "create_loan_record",
          "get_loan_records"
        ],
        "route_count": 2,
        "verification_hash": "5ec92e22a07df9682e726e87c35c2aa9283a64656f52fff6208a0b0bd557ab01"
      }
    }
  ],
  "started_at": "2026-10-14T12:19:12.619956+00:00",
  "workspace_id": "007518e7-2462-43d5-9206-ad0a779472c6",
  "feature_id": "capability_record_item_and_borrower_3af7a315",
  "screen_id": null,
  "expected_workspace_version": 3,
  "session_id": "50237586-586f-424b-b23b-e6a24c7f6b29",
  "mvp_session_id": "45526ed8-d80d-44c2-b25d-6440dc4ff343",
  "source": {
    "architecture_backend_hash": "f5bb3a07d15cbae76be20c15c4d57f239863d33b1d0693b71fe9e7598442270d",
    "database_feature_sql_hash": "a9d0d5cf6d37a2d8838d6a162027ebf4392b0d35c71572bd912f127f3d9682d3"
  },
  "outcome": "completed",
  "finished_at": "2026-10-14T12:19:24.041139+00:00"
}
```

### Checked output matches packaged files

```json
{
  "stage": "backend feature",
  "feature": "capability_view_loan_list_e3bf329c",
  "screen": null,
  "outcome": "completed"
}
```

```json
{
  "stage": "backend feature",
  "tool_slug": "backend-generator",
  "checks": [
    {
      "check": "Backend syntax, functions and routes",
      "status": "passed",
      "files": [
        {
          "path": "backend/features/view_loan_list/feature.py",
          "sha256": "86b91f44d6db397825f42b8bc28de10f367bd8fdf43f59d28b1a686303f5b6ac"
        }
      ],
      "result": {
        "valid": true,
        "feature_id": "capability_view_loan_list_e3bf329c",
        "file_count": 1,
        "function_ids": [
          "capability_view_loan_list_e3bf329c.function.get_loans"
        ],
        "function_names": [
          "get_loans"
        ],
        "route_count": 1,
        "verification_hash": "f624e965d6285f7c1a07d7cd8c037678503a78f95c75cc01c41479f07288177c"
      }
    }
  ],
  "started_at": "2026-10-14T12:19:26.721073+00:00",
  "workspace_id": "007518e7-2462-43d5-9206-ad0a779472c6",
  "feature_id": "capability_view_loan_list_e3bf329c",
  "screen_id": null,
  "expected_workspace_version": 5,
  "session_id": "50237586-586f-424b-b23b-e6a24c7f6b29",
  "mvp_session_id": "45526ed8-d80d-44c2-b25d-6440dc4ff343",
  "source": {
    "architecture_backend_hash": "66a14995095325e435f358178b6431518e8a0fcb363fa8d8a0a4f45e27992824",
    "database_feature_sql_hash": "5bb71981b69e4d6dbd7baff687099bc0c2ae7ac2cf9d73a5c2f54f30361a7252"
  },
  "outcome": "completed",
  "finished_at": "2026-10-14T12:19:33.068620+00:00"
}
```

### Checked output matches packaged files

```json
{
  "stage": "backend feature",
  "feature": "capability_character_limit_validation_533aef43",
  "screen": null,
  "outcome": "completed"
}
```

```json
{
  "stage": "backend feature",
  "tool_slug": "backend-generator",
  "checks": [
    {
      "check": "Backend syntax, functions and routes",
      "status": "passed",
      "files": [
        {
          "path": "backend/features/character_limit_validation/feature.py",
          "sha256": "f07491fc4255230ef0e9214fb8794018d626777fa01c827a0685c323f34d47ad"
        }
      ],
      "result": {
        "valid": true,
        "feature_id": "capability_character_limit_validation_533aef43",
        "file_count": 1,
        "function_ids": [],
        "function_names": [],
        "route_count": 0,
        "verification_hash": "91214185391bcb5e305b11e2f18808eef5aee7679250c88640f061e4e3a3ede6"
      }
    }
  ],
  "started_at": "2026-10-14T12:19:36.539312+00:00",
  "workspace_id": "007518e7-2462-43d5-9206-ad0a779472c6",
  "feature_id": "capability_character_limit_validation_533aef43",
  "screen_id": null,
  "expected_workspace_version": 7,
  "session_id": "50237586-586f-424b-b23b-e6a24c7f6b29",
  "mvp_session_id": "45526ed8-d80d-44c2-b25d-6440dc4ff343",
  "source": {
    "architecture_backend_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "database_feature_sql_hash": "9d851035071f18daebefdf2c894be63680e1db252013dea94c7eaed76e109616"
  },
  "outcome": "completed",
  "finished_at": "2026-10-14T12:19:48.212270+00:00"
}
```

### Checked output matches packaged files

```json
{
  "stage": "backend feature",
  "feature": "capability_required_field_validation_18c05c66",
  "screen": null,
  "outcome": "completed"
}
```

```json
{
  "stage": "backend feature",
  "tool_slug": "backend-generator",
  "checks": [
    {
      "check": "Backend syntax, functions and routes",
      "status": "passed",
      "files": [
        {
          "path": "backend/features/required_field_validation/feature.py",
          "sha256": "14e4465ec3b3e06a5030d3ee20aa514c5523b0870beb3b9b711e6dbdc9ced517"
        }
      ],
      "result": {
        "valid": true,
        "feature_id": "capability_required_field_validation_18c05c66",
        "file_count": 1,
        "function_ids": [],
        "function_names": [],
        "route_count": 3,
        "verification_hash": "f1bc90b92814bd4686c08abf9fa8e48a24f562c1756809b7b194751181407242"
      }
    }
  ],
  "started_at": "2026-10-14T12:19:51.482886+00:00",
  "workspace_id": "007518e7-2462-43d5-9206-ad0a779472c6",
  "feature_id": "capability_required_field_validation_18c05c66",
  "screen_id": null,
  "expected_workspace_version": 9,
  "session_id": "50237586-586f-424b-b23b-e6a24c7f6b29",
  "mvp_session_id": "45526ed8-d80d-44c2-b25d-6440dc4ff343",
  "source": {
    "architecture_backend_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "database_feature_sql_hash": "dc438b2ed3103715511021f9fba2b51f56365113cf9b858bffee30371459fe04"
  },
  "outcome": "completed",
  "finished_at": "2026-10-14T12:20:02.536073+00:00"
}
```

### Checked output matches packaged files

```json
{
  "stage": "backend feature",
  "feature": "capability_single_screen_layout_3203f8ec",
  "screen": null,
  "outcome": "completed"
}
```

```json
{
  "stage": "backend feature",
  "tool_slug": "backend-generator",
  "checks": [
    {
      "check": "Backend syntax, functions and routes",
      "status": "passed",
      "files": [
        {
          "path": "backend/features/single_screen_layout/feature.py",
          "sha256": "86e7a6c2fe15130ba110911be33d25dc4aafe0ff56f12cdd4e30a577259d2a35"
        }
      ],
      "result": {
        "valid": true,
        "feature_id": "capability_single_screen_layout_3203f8ec",
        "file_count": 1,
        "function_ids": [],
        "function_names": [],
        "route_count": 6,
        "verification_hash": "d2faa62329b6999d019e4337bce55bc9221acc055b4a5332d9a8bbb3fdd92964"
      }
    }
  ],
  "started_at": "2026-10-14T12:20:06.160700+00:00",
  "workspace_id": "007518e7-2462-43d5-9206-ad0a779472c6",
  "feature_id": "capability_single_screen_layout_3203f8ec",
  "screen_id": null,
  "expected_workspace_version": 11,
  "session_id": "50237586-586f-424b-b23b-e6a24c7f6b29",
  "mvp_session_id": "45526ed8-d80d-44c2-b25d-6440dc4ff343",
  "source": {
    "architecture_backend_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "database_feature_sql_hash": "ff2501f9eea3bcb0b3e9630509374a2c0ec261bae07d5cf0dda2e0235f934bea"
  },
  "outcome": "completed",
  "finished_at": "2026-10-14T12:20:22.046800+00:00"
}
```

### Checked output matches packaged files

```json
{
  "stage": "backend feature",
  "feature": "capability_inline_error_messages_9ddfedf0",
  "screen": null,
  "outcome": "completed"
}
```

```json
{
  "stage": "backend feature",
  "tool_slug": "backend-generator",
  "checks": [
    {
      "check": "Backend syntax, functions and routes",
      "status": "passed",
      "files": [
        {
          "path": "backend/features/inline_error_messages/feature.py",
          "sha256": "85ac1441eecf057f2e9a59bf898a542126faad01724cdbd77ef0692033f76f66"
        }
      ],
      "result": {
        "valid": true,
        "feature_id": "capability_inline_error_messages_9ddfedf0",
        "file_count": 1,
        "function_ids": [],
        "function_names": [],
        "route_count": 0,
        "verification_hash": "33409b62c5412a5acec10d9b80b56deedb0c001538c370b24b1af3deba4d3b64"
      }
    }
  ],
  "started_at": "2026-10-14T12:20:26.179238+00:00",
  "workspace_id": "007518e7-2462-43d5-9206-ad0a779472c6",
  "feature_id": "capability_inline_error_messages_9ddfedf0",
  "screen_id": null,
  "expected_workspace_version": 13,
  "session_id": "50237586-586f-424b-b23b-e6a24c7f6b29",
  "mvp_session_id": "45526ed8-d80d-44c2-b25d-6440dc4ff343",
  "source": {
    "architecture_backend_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "database_feature_sql_hash": "66c535ace49f2ee734f9b288cafc87675d134bc78717748d33c879619d94d38a"
  },
  "outcome": "completed",
  "finished_at": "2026-10-14T12:20:55.275527+00:00"
}
```

### Historical attempt; not evidence of a current defect

```json
{
  "stage": "backend assembly",
  "feature": null,
  "screen": null,
  "outcome": "completed"
}
```

```json
{
  "stage": "backend assembly",
  "tool_slug": "backend-generator",
  "checks": [],
  "started_at": "2026-10-14T12:20:58.546460+00:00",
  "workspace_id": "007518e7-2462-43d5-9206-ad0a779472c6",
  "feature_id": null,
  "screen_id": null,
  "expected_workspace_version": 14,
  "session_id": "50237586-586f-424b-b23b-e6a24c7f6b29",
  "mvp_session_id": "45526ed8-d80d-44c2-b25d-6440dc4ff343",
  "source": {},
  "outcome": "completed",
  "finished_at": "2026-10-14T12:20:58.899456+00:00"
}
```
