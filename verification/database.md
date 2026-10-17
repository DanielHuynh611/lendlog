# Database verification

SQL assembly concatenates the approved feature SQL into `database/schema.sql`. Generation checks table coverage and SQL structure; it does not execute the schema against MySQL. Constraints, migrations and queries have not been proven by these checks.

```json
{
  "records": [
    {
      "session_id": "b8f5b476-cad8-46f4-9903-5699b690c3e0",
      "source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604",
      "state": "completed",
      "manifest_hash": "8dd35d71d0cb80757045321b48734f73fa4a3732b79d8fefc33af39e3690f8b3"
    }
  ]
}
```

## Current SQL revisions

```json
{
  "records": [
    {
      "feature_id": "capability_local_browser_storage_03ab1d7c",
      "state": "approved",
      "revision": 1,
      "last_run_id": "658423a3-4ea9-4c44-a6bf-164d3474f733",
      "last_error_code": null,
      "last_error_details": null
    },
    {
      "feature_id": "capability_record_item_and_borrower_3af7a315",
      "state": "approved",
      "revision": 1,
      "last_run_id": "62621205-63c5-4b77-9123-a475c650092a",
      "last_error_code": null,
      "last_error_details": null
    },
    {
      "feature_id": "capability_view_loan_list_e3bf329c",
      "state": "approved",
      "revision": 1,
      "last_run_id": "b4eccddd-140c-4d65-9246-2852da44f0e1",
      "last_error_code": null,
      "last_error_details": null
    },
    {
      "feature_id": "capability_character_limit_validation_533aef43",
      "state": "approved",
      "revision": 1,
      "last_run_id": "5fe6baa0-2903-41c8-bb87-758e293f872f",
      "last_error_code": null,
      "last_error_details": null
    },
    {
      "feature_id": "capability_required_field_validation_18c05c66",
      "state": "approved",
      "revision": 1,
      "last_run_id": "8dd24cb3-47bd-4018-b5f4-67e42c1479cc",
      "last_error_code": null,
      "last_error_details": null
    },
    {
      "feature_id": "capability_single_screen_layout_3203f8ec",
      "state": "approved",
      "revision": 1,
      "last_run_id": "7a63387e-b8fb-42d4-bc60-fd472b097955",
      "last_error_code": null,
      "last_error_details": null
    },
    {
      "feature_id": "capability_inline_error_messages_9ddfedf0",
      "state": "approved",
      "revision": 1,
      "last_run_id": "a5c2e934-651f-49d4-9335-3e836dbe72ab",
      "last_error_code": null,
      "last_error_details": null
    }
  ]
}
```

## Run history
Compare each feature's last_run_id with these run IDs. Failed/superseded runs are historical; compare source hashes.

```json
{
  "records": [
    {
      "id": "658423a3-4ea9-4c44-a6bf-164d3474f733",
      "scope_key": "feature:capability_local_browser_storage_03ab1d7c",
      "kind": "feature_generate",
      "status": "succeeded",
      "expected_source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604",
      "created_at": "2026-10-14 12:18:01",
      "finished_at": "2026-10-14 12:18:04",
      "error_code": null,
      "error_details": [],
      "provider_attempts": [
        {
          "phase": "initial",
          "outcome": "candidate",
          "provider": "openai",
          "duration_ms": 2619,
          "stop_reason": "tool_use",
          "timeout_seconds": 70
        }
      ]
    },
    {
      "id": "62621205-63c5-4b77-9123-a475c650092a",
      "scope_key": "feature:capability_record_item_and_borrower_3af7a315",
      "kind": "feature_generate",
      "status": "succeeded",
      "expected_source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604",
      "created_at": "2026-10-14 12:18:19",
      "finished_at": "2026-10-14 12:18:21",
      "error_code": null,
      "error_details": [],
      "provider_attempts": [
        {
          "phase": "initial",
          "outcome": "candidate",
          "provider": "openai",
          "duration_ms": 1886,
          "stop_reason": "tool_use",
          "timeout_seconds": 70
        }
      ]
    },
    {
      "id": "b4eccddd-140c-4d65-9246-2852da44f0e1",
      "scope_key": "feature:capability_view_loan_list_e3bf329c",
      "kind": "feature_generate",
      "status": "succeeded",
      "expected_source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604",
      "created_at": "2026-10-14 12:18:23",
      "finished_at": "2026-10-14 12:18:25",
      "error_code": null,
      "error_details": [],
      "provider_attempts": [
        {
          "phase": "initial",
          "outcome": "candidate",
          "provider": "openai",
          "duration_ms": 1718,
          "stop_reason": "tool_use",
          "timeout_seconds": 70
        }
      ]
    },
    {
      "id": "5fe6baa0-2903-41c8-bb87-758e293f872f",
      "scope_key": "feature:capability_character_limit_validation_533aef43",
      "kind": "feature_generate",
      "status": "succeeded",
      "expected_source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604",
      "created_at": "2026-10-14 12:18:29",
      "finished_at": "2026-10-14 12:18:29",
      "error_code": null,
      "error_details": [],
      "provider_attempts": []
    },
    {
      "id": "8dd24cb3-47bd-4018-b5f4-67e42c1479cc",
      "scope_key": "feature:capability_required_field_validation_18c05c66",
      "kind": "feature_generate",
      "status": "succeeded",
      "expected_source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604",
      "created_at": "2026-10-14 12:18:31",
      "finished_at": "2026-10-14 12:18:31",
      "error_code": null,
      "error_details": [],
      "provider_attempts": []
    },
    {
      "id": "7a63387e-b8fb-42d4-bc60-fd472b097955",
      "scope_key": "feature:capability_single_screen_layout_3203f8ec",
      "kind": "feature_generate",
      "status": "succeeded",
      "expected_source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604",
      "created_at": "2026-10-14 12:18:34",
      "finished_at": "2026-10-14 12:18:34",
      "error_code": null,
      "error_details": [],
      "provider_attempts": []
    },
    {
      "id": "a5c2e934-651f-49d4-9335-3e836dbe72ab",
      "scope_key": "feature:capability_inline_error_messages_9ddfedf0",
      "kind": "feature_generate",
      "status": "succeeded",
      "expected_source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604",
      "created_at": "2026-10-14 12:18:37",
      "finished_at": "2026-10-14 12:18:37",
      "error_code": null,
      "error_details": [],
      "provider_attempts": []
    }
  ]
}
```


For a recorded table/SQL error, inspect the identified table in `database/schema.sql` and the run details. Apply the schema to a local MySQL database following the README to obtain actual database execution results. If no cause or location was captured, it is unknown; missing history is not a pass.
