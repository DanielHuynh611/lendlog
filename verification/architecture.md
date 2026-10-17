# Architecture verification

These are contract and coverage checks, not executable application tests. Non-blocking findings describe issues intentionally retained in the generated files for you to inspect and repair. They do not mean the package is missing. Historical attempts may refer to an earlier scope; compare scope hashes.

## Findings and next steps

```json
{
  "finding": "cross_feature_table_concept_overlap",
  "code": "cross_feature_table_concept_overlap",
  "severity": "error",
  "blocking": false,
  "category": "database",
  "message": "Multiple features define separate tables for the same likely 'loan' concept.",
  "affected_feature_ids": [
    "capability_local_browser_storage_03ab1d7c",
    "capability_record_item_and_borrower_3af7a315",
    "capability_view_loan_list_e3bf329c"
  ],
  "components": [
    {
      "feature_id": "capability_local_browser_storage_03ab1d7c",
      "component_id": "capability_local_browser_storage_03ab1d7c.table.loan_records",
      "name": "f_03ab1d7c__loan_records"
    },
    {
      "feature_id": "capability_record_item_and_borrower_3af7a315",
      "component_id": "capability_record_item_and_borrower_3af7a315.table.loan_records",
      "name": "f_3af7a315__loan_records"
    },
    {
      "feature_id": "capability_view_loan_list_e3bf329c",
      "component_id": "capability_view_loan_list_e3bf329c.table.loans",
      "name": "f_e3bf329c__loans"
    }
  ],
  "repair": "Inspect whether these tables represent one shared entity. If they do, keep one canonical table and update the affected feature queries and relationships."
}
```

Multiple features define separate tables for the same likely 'loan' concept. Inspect whether these tables represent one shared entity. If they do, keep one canonical table and update the affected feature queries and relationships.

```json
{
  "finding": "cross_feature_screen_route_collision",
  "code": "cross_feature_screen_route_collision",
  "severity": "error",
  "blocking": false,
  "category": "frontend",
  "message": "Multiple features define screens for the same route '/'.",
  "affected_feature_ids": [
    "capability_character_limit_validation_533aef43",
    "capability_inline_error_messages_9ddfedf0",
    "capability_local_browser_storage_03ab1d7c",
    "capability_record_item_and_borrower_3af7a315",
    "capability_required_field_validation_18c05c66",
    "capability_single_screen_layout_3203f8ec",
    "capability_view_loan_list_e3bf329c"
  ],
  "components": [
    {
      "feature_id": "capability_character_limit_validation_533aef43",
      "component_id": "capability_character_limit_validation_533aef43.screen.main_loan_entry",
      "name": "Main Loan Entry Screen",
      "route": "/"
    },
    {
      "feature_id": "capability_inline_error_messages_9ddfedf0",
      "component_id": "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors",
      "name": "Main Form with Inline Error Messages",
      "route": "/"
    },
    {
      "feature_id": "capability_local_browser_storage_03ab1d7c",
      "component_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
      "name": "Main Loan List",
      "route": "/"
    },
    {
      "feature_id": "capability_record_item_and_borrower_3af7a315",
      "component_id": "capability_record_item_and_borrower_3af7a315.screen.loan_entry",
      "name": "Loan Entry Screen",
      "route": "/"
    },
    {
      "feature_id": "capability_required_field_validation_18c05c66",
      "component_id": "capability_required_field_validation_18c05c66.screen.loan_entry_form",
      "name": "Loan Entry Form with Validation",
      "route": "/"
    },
    {
      "feature_id": "capability_single_screen_layout_3203f8ec",
      "component_id": "capability_single_screen_layout_3203f8ec.screen.main",
      "name": "Main Screen",
      "route": "/"
    },
    {
      "feature_id": "capability_view_loan_list_e3bf329c",
      "component_id": "capability_view_loan_list_e3bf329c.screen.loan_list",
      "name": "Loan List",
      "route": "/"
    }
  ],
  "repair": "Decide whether these responsibilities belong on one shared screen. Merge the screen behavior or assign distinct routes, then update navigation and actions."
}
```

Multiple features define screens for the same route '/'. Decide whether these responsibilities belong on one shared screen. Merge the screen behavior or assign distinct routes, then update navigation and actions.

## Current blueprint
```json
{
  "source": {
    "scope_id": "scope_lendlog_bdfde953",
    "source_session_id": "45526ed8-d80d-44c2-b25d-6440dc4ff343",
    "source_hash": "9d82d1b676a6cb03a88f341ab75048245f4f077016f30afe533721070a20f604"
  },
  "blueprint_hash": "b7d4176746957966770bdca68fd36e9f641633c049c17eb8938090ff5be474f5",
  "assembly": {
    "valid": true,
    "status": "generated_with_issues",
    "errors": [],
    "non_blocking_errors": [
      {
        "code": "cross_feature_table_concept_overlap",
        "severity": "error",
        "blocking": false,
        "category": "database",
        "message": "Multiple features define separate tables for the same likely 'loan' concept.",
        "affected_feature_ids": [
          "capability_local_browser_storage_03ab1d7c",
          "capability_record_item_and_borrower_3af7a315",
          "capability_view_loan_list_e3bf329c"
        ],
        "components": [
          {
            "feature_id": "capability_local_browser_storage_03ab1d7c",
            "component_id": "capability_local_browser_storage_03ab1d7c.table.loan_records",
            "name": "f_03ab1d7c__loan_records"
          },
          {
            "feature_id": "capability_record_item_and_borrower_3af7a315",
            "component_id": "capability_record_item_and_borrower_3af7a315.table.loan_records",
            "name": "f_3af7a315__loan_records"
          },
          {
            "feature_id": "capability_view_loan_list_e3bf329c",
            "component_id": "capability_view_loan_list_e3bf329c.table.loans",
            "name": "f_e3bf329c__loans"
          }
        ],
        "repair": "Inspect whether these tables represent one shared entity. If they do, keep one canonical table and update the affected feature queries and relationships."
      },
      {
        "code": "cross_feature_screen_route_collision",
        "severity": "error",
        "blocking": false,
        "category": "frontend",
        "message": "Multiple features define screens for the same route '/'.",
        "affected_feature_ids": [
          "capability_character_limit_validation_533aef43",
          "capability_inline_error_messages_9ddfedf0",
          "capability_local_browser_storage_03ab1d7c",
          "capability_record_item_and_borrower_3af7a315",
          "capability_required_field_validation_18c05c66",
          "capability_single_screen_layout_3203f8ec",
          "capability_view_loan_list_e3bf329c"
        ],
        "components": [
          {
            "feature_id": "capability_character_limit_validation_533aef43",
            "component_id": "capability_character_limit_validation_533aef43.screen.main_loan_entry",
            "name": "Main Loan Entry Screen",
            "route": "/"
          },
          {
            "feature_id": "capability_inline_error_messages_9ddfedf0",
            "component_id": "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors",
            "name": "Main Form with Inline Error Messages",
            "route": "/"
          },
          {
            "feature_id": "capability_local_browser_storage_03ab1d7c",
            "component_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
            "name": "Main Loan List",
            "route": "/"
          },
          {
            "feature_id": "capability_record_item_and_borrower_3af7a315",
            "component_id": "capability_record_item_and_borrower_3af7a315.screen.loan_entry",
            "name": "Loan Entry Screen",
            "route": "/"
          },
          {
            "feature_id": "capability_required_field_validation_18c05c66",
            "component_id": "capability_required_field_validation_18c05c66.screen.loan_entry_form",
            "name": "Loan Entry Form with Validation",
            "route": "/"
          },
          {
            "feature_id": "capability_single_screen_layout_3203f8ec",
            "component_id": "capability_single_screen_layout_3203f8ec.screen.main",
            "name": "Main Screen",
            "route": "/"
          },
          {
            "feature_id": "capability_view_loan_list_e3bf329c",
            "component_id": "capability_view_loan_list_e3bf329c.screen.loan_list",
            "name": "Loan List",
            "route": "/"
          }
        ],
        "repair": "Decide whether these responsibilities belong on one shared screen. Merge the screen behavior or assign distinct routes, then update navigation and actions."
      }
    ],
    "non_blocking_error_count": 2
  },
  "coverage": {
    "valid": true,
    "features": {
      "covered": 7,
      "total": 7
    },
    "acceptance_criteria": {
      "covered": 22,
      "total": 22
    }
  },
  "features": [
    {
      "feature_id": "capability_local_browser_storage_03ab1d7c",
      "verification": {
        "valid": true,
        "feature_id": "capability_local_browser_storage_03ab1d7c",
        "criteria": [
          {
            "criterion_id": "criterion_done_when_clearing_browser_site_data_removes_all_b56a0105",
            "table_ids": [
              "capability_local_browser_storage_03ab1d7c.table.loan_records"
            ],
            "function_ids": [],
            "screen_ids": [
              "capability_local_browser_storage_03ab1d7c.screen.main_loan_list"
            ]
          },
          {
            "criterion_id": "criterion_done_when_loan_records_saved_in_one_session_are__1d03af03",
            "table_ids": [
              "capability_local_browser_storage_03ab1d7c.table.loan_records"
            ],
            "function_ids": [
              "capability_local_browser_storage_03ab1d7c.function.create_loan_record",
              "capability_local_browser_storage_03ab1d7c.function.get_all_loan_records"
            ],
            "screen_ids": [
              "capability_local_browser_storage_03ab1d7c.screen.main_loan_list"
            ]
          },
          {
            "criterion_id": "criterion_done_when_records_are_stored_in_browser_local_st_fc62bf0f",
            "table_ids": [
              "capability_local_browser_storage_03ab1d7c.table.loan_records"
            ],
            "function_ids": [
              "capability_local_browser_storage_03ab1d7c.function.create_loan_record",
              "capability_local_browser_storage_03ab1d7c.function.get_all_loan_records"
            ],
            "screen_ids": [
              "capability_local_browser_storage_03ab1d7c.screen.main_loan_list"
            ]
          }
        ],
        "traces": [
          {
            "screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
            "action_id": "capability_local_browser_storage_03ab1d7c.screen-action.load_loans_on_page_open",
            "function_id": "capability_local_browser_storage_03ab1d7c.function.get_all_loan_records",
            "table_ids": [
              "capability_local_browser_storage_03ab1d7c.table.loan_records"
            ]
          },
          {
            "screen_id": "capability_local_browser_storage_03ab1d7c.screen.main_loan_list",
            "action_id": "capability_local_browser_storage_03ab1d7c.screen-action.create_new_loan",
            "function_id": "capability_local_browser_storage_03ab1d7c.function.create_loan_record",
            "table_ids": [
              "capability_local_browser_storage_03ab1d7c.table.loan_records"
            ]
          }
        ],
        "errors": []
      }
    },
    {
      "feature_id": "capability_record_item_and_borrower_3af7a315",
      "verification": {
        "valid": true,
        "feature_id": "capability_record_item_and_borrower_3af7a315",
        "criteria": [
          {
            "criterion_id": "criterion_done_when_clicking_save_creates_a_new_loan_recor_add2ef9f",
            "table_ids": [
              "capability_record_item_and_borrower_3af7a315.table.loan_records"
            ],
            "function_ids": [
              "capability_record_item_and_borrower_3af7a315.function.create_loan_record",
              "capability_record_item_and_borrower_3af7a315.function.get_loan_records"
            ],
            "screen_ids": [
              "capability_record_item_and_borrower_3af7a315.screen.loan_entry"
            ]
          },
          {
            "criterion_id": "criterion_done_when_leading_and_trailing_spaces_are_automa_8658b673",
            "table_ids": [
              "capability_record_item_and_borrower_3af7a315.table.loan_records"
            ],
            "function_ids": [
              "capability_record_item_and_borrower_3af7a315.function.create_loan_record"
            ],
            "screen_ids": [
              "capability_record_item_and_borrower_3af7a315.screen.loan_entry"
            ]
          },
          {
            "criterion_id": "criterion_done_when_the_form_fields_clear_after_successful_4e7ae2a7",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_record_item_and_borrower_3af7a315.screen.loan_entry"
            ]
          },
          {
            "criterion_id": "criterion_done_when_the_form_has_two_text_input_fields_lab_26574d5d",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_record_item_and_borrower_3af7a315.screen.loan_entry"
            ]
          }
        ],
        "traces": [
          {
            "screen_id": "capability_record_item_and_borrower_3af7a315.screen.loan_entry",
            "action_id": "capability_record_item_and_borrower_3af7a315.screen-action.save_loan",
            "function_id": "capability_record_item_and_borrower_3af7a315.function.create_loan_record",
            "table_ids": [
              "capability_record_item_and_borrower_3af7a315.table.loan_records"
            ]
          },
          {
            "screen_id": "capability_record_item_and_borrower_3af7a315.screen.loan_entry",
            "action_id": "capability_record_item_and_borrower_3af7a315.screen-action.load_loans",
            "function_id": "capability_record_item_and_borrower_3af7a315.function.get_loan_records",
            "table_ids": [
              "capability_record_item_and_borrower_3af7a315.table.loan_records"
            ]
          }
        ],
        "errors": []
      }
    },
    {
      "feature_id": "capability_view_loan_list_e3bf329c",
      "verification": {
        "valid": true,
        "feature_id": "capability_view_loan_list_e3bf329c",
        "criteria": [
          {
            "criterion_id": "criterion_done_when_all_saved_loan_records_are_displayed_i_3b937b45",
            "table_ids": [
              "capability_view_loan_list_e3bf329c.table.loans"
            ],
            "function_ids": [
              "capability_view_loan_list_e3bf329c.function.get_loans"
            ],
            "screen_ids": [
              "capability_view_loan_list_e3bf329c.screen.loan_list"
            ]
          },
          {
            "criterion_id": "criterion_done_when_each_list_item_shows_both_the_item_nam_14c58b5d",
            "table_ids": [
              "capability_view_loan_list_e3bf329c.table.loans"
            ],
            "function_ids": [
              "capability_view_loan_list_e3bf329c.function.get_loans"
            ],
            "screen_ids": [
              "capability_view_loan_list_e3bf329c.screen.loan_list"
            ]
          },
          {
            "criterion_id": "criterion_done_when_the_list_updates_immediately_after_sav_e512e632",
            "table_ids": [
              "capability_view_loan_list_e3bf329c.table.loans"
            ],
            "function_ids": [
              "capability_view_loan_list_e3bf329c.function.get_loans"
            ],
            "screen_ids": [
              "capability_view_loan_list_e3bf329c.screen.loan_list"
            ]
          },
          {
            "criterion_id": "criterion_done_when_the_newest_loans_appear_first_in_the_l_c9026649",
            "table_ids": [
              "capability_view_loan_list_e3bf329c.table.loans"
            ],
            "function_ids": [
              "capability_view_loan_list_e3bf329c.function.get_loans"
            ],
            "screen_ids": [
              "capability_view_loan_list_e3bf329c.screen.loan_list"
            ]
          }
        ],
        "traces": [
          {
            "screen_id": "capability_view_loan_list_e3bf329c.screen.loan_list",
            "action_id": "capability_view_loan_list_e3bf329c.screen-action.load_loans",
            "function_id": "capability_view_loan_list_e3bf329c.function.get_loans",
            "table_ids": [
              "capability_view_loan_list_e3bf329c.table.loans"
            ]
          },
          {
            "screen_id": "capability_view_loan_list_e3bf329c.screen.loan_list",
            "action_id": "capability_view_loan_list_e3bf329c.screen-action.refresh_loans",
            "function_id": "capability_view_loan_list_e3bf329c.function.get_loans",
            "table_ids": [
              "capability_view_loan_list_e3bf329c.table.loans"
            ]
          }
        ],
        "errors": []
      }
    },
    {
      "feature_id": "capability_character_limit_validation_533aef43",
      "verification": {
        "valid": true,
        "feature_id": "capability_character_limit_validation_533aef43",
        "criteria": [],
        "traces": [],
        "errors": []
      }
    },
    {
      "feature_id": "capability_required_field_validation_18c05c66",
      "verification": {
        "valid": true,
        "feature_id": "capability_required_field_validation_18c05c66",
        "criteria": [
          {
            "criterion_id": "criterion_done_when_attempting_to_save_with_an_empty_borro_27356e60",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_required_field_validation_18c05c66.screen.loan_entry_form"
            ]
          },
          {
            "criterion_id": "criterion_done_when_attempting_to_save_with_an_empty_item__7849d11e",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_required_field_validation_18c05c66.screen.loan_entry_form"
            ]
          },
          {
            "criterion_id": "criterion_done_when_both_fields_must_contain_at_least_one__a99882b9",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_required_field_validation_18c05c66.screen.loan_entry_form"
            ]
          }
        ],
        "traces": [],
        "errors": []
      }
    },
    {
      "feature_id": "capability_single_screen_layout_3203f8ec",
      "verification": {
        "valid": true,
        "feature_id": "capability_single_screen_layout_3203f8ec",
        "criteria": [
          {
            "criterion_id": "criterion_done_when_no_navigation_or_page_changes_are_requ_787e9c22",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_single_screen_layout_3203f8ec.screen.main"
            ]
          },
          {
            "criterion_id": "criterion_done_when_the_item_and_borrower_input_fields_are_870cdf87",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_single_screen_layout_3203f8ec.screen.main"
            ]
          },
          {
            "criterion_id": "criterion_done_when_the_loan_list_is_visible_below_the_for_7c351a7b",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_single_screen_layout_3203f8ec.screen.main"
            ]
          },
          {
            "criterion_id": "criterion_done_when_the_save_button_is_visible_below_or_ne_ad3ce617",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_single_screen_layout_3203f8ec.screen.main"
            ]
          }
        ],
        "traces": [],
        "errors": []
      }
    },
    {
      "feature_id": "capability_inline_error_messages_9ddfedf0",
      "verification": {
        "valid": true,
        "feature_id": "capability_inline_error_messages_9ddfedf0",
        "criteria": [
          {
            "criterion_id": "criterion_done_when_an_error_message_appears_near_the_borr_e07899db",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors"
            ]
          },
          {
            "criterion_id": "criterion_done_when_an_error_message_appears_near_the_item_6740dc5c",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors"
            ]
          },
          {
            "criterion_id": "criterion_done_when_error_messages_are_short_clear_and_dis_c5c85117",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors"
            ]
          },
          {
            "criterion_id": "criterion_done_when_error_messages_disappear_once_the_user_fc634397",
            "table_ids": [],
            "function_ids": [],
            "screen_ids": [
              "capability_inline_error_messages_9ddfedf0.screen.main_form_with_inline_errors"
            ]
          }
        ],
        "traces": [],
        "errors": []
      }
    }
  ]
}
```

## Historical validation attempts
```json
{
  "records": [
    {
      "feature_id": "capability_local_browser_storage_03ab1d7c",
      "stage": "database",
      "outcome": "succeeded",
      "scope_hash": "570878f318efd780897f77222f7442468c33b2053581ce9db2fa10b6f7151a54",
      "created_at": "2026-10-14 12:10:40",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_local_browser_storage_03ab1d7c",
      "stage": "backend",
      "outcome": "succeeded",
      "scope_hash": "400b83e166a29253d6aaebb9865e336bd90dd005dd2648f12b725c495c9478db",
      "created_at": "2026-10-14 12:11:03",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_local_browser_storage_03ab1d7c",
      "stage": "screens",
      "outcome": "succeeded",
      "scope_hash": "230e70a0e827dd1ad9324fbd3662279be55b034a7498d20ca48a98b349bd0bf7",
      "created_at": "2026-10-14 12:11:27",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_record_item_and_borrower_3af7a315",
      "stage": "database",
      "outcome": "succeeded",
      "scope_hash": "570878f318efd780897f77222f7442468c33b2053581ce9db2fa10b6f7151a54",
      "created_at": "2026-10-14 12:11:49",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_record_item_and_borrower_3af7a315",
      "stage": "backend",
      "outcome": "succeeded",
      "scope_hash": "1cdd747d5c20fcfa7010467b7a877eb383108ead8b35d4b31905940711afc347",
      "created_at": "2026-10-14 12:12:14",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_record_item_and_borrower_3af7a315",
      "stage": "screens",
      "outcome": "succeeded",
      "scope_hash": "781eef45526297fb2af4b46a64a5bf8ccd5287f6471c9de216f3eca33edd587b",
      "created_at": "2026-10-14 12:12:40",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_view_loan_list_e3bf329c",
      "stage": "database",
      "outcome": "succeeded",
      "scope_hash": "570878f318efd780897f77222f7442468c33b2053581ce9db2fa10b6f7151a54",
      "created_at": "2026-10-14 12:13:15",
      "last_error_code": null,
      "attempts": [
        {
          "code": "invalid_feature_database",
          "status": "validation_failed",
          "attempt": 1,
          "retryable": true,
          "detail_categories": [
            "table_usage_field_unresolved",
            "table_usage_unresolved"
          ]
        },
        {
          "code": null,
          "status": "accepted",
          "attempt": 2,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_view_loan_list_e3bf329c",
      "stage": "backend",
      "outcome": "succeeded",
      "scope_hash": "8f29794e606ef6078ab0114518d64bb901ffe20ad0019af57fb9b9b59d4da934",
      "created_at": "2026-10-14 12:13:31",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_view_loan_list_e3bf329c",
      "stage": "screens",
      "outcome": "succeeded",
      "scope_hash": "80769c08b39c1cfe13631de705b6c01ed65f88a7bd1e5b0736e8f583e771822b",
      "created_at": "2026-10-14 12:13:50",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_character_limit_validation_533aef43",
      "stage": "database",
      "outcome": "succeeded",
      "scope_hash": "570878f318efd780897f77222f7442468c33b2053581ce9db2fa10b6f7151a54",
      "created_at": "2026-10-14 12:14:06",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_character_limit_validation_533aef43",
      "stage": "backend",
      "outcome": "succeeded",
      "scope_hash": "789e6ff2ece8ae773a4e28646cc54ab34d85a67a1a193fcae51cb505b8b33272",
      "created_at": "2026-10-14 12:14:19",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_character_limit_validation_533aef43",
      "stage": "screens",
      "outcome": "succeeded",
      "scope_hash": "0068dc9f1ae726d17d8c3e9c5318e4cbfc6337737d7475183017cf2817b8ed26",
      "created_at": "2026-10-14 12:14:37",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_required_field_validation_18c05c66",
      "stage": "database",
      "outcome": "succeeded",
      "scope_hash": "570878f318efd780897f77222f7442468c33b2053581ce9db2fa10b6f7151a54",
      "created_at": "2026-10-14 12:14:52",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_required_field_validation_18c05c66",
      "stage": "backend",
      "outcome": "succeeded",
      "scope_hash": "5b0eb6816fad72d111b84e0952546442162ab06662afb026b383d7b008191f65",
      "created_at": "2026-10-14 12:15:06",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_required_field_validation_18c05c66",
      "stage": "screens",
      "outcome": "succeeded",
      "scope_hash": "0068dc9f1ae726d17d8c3e9c5318e4cbfc6337737d7475183017cf2817b8ed26",
      "created_at": "2026-10-14 12:15:37",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_single_screen_layout_3203f8ec",
      "stage": "database",
      "outcome": "succeeded",
      "scope_hash": "570878f318efd780897f77222f7442468c33b2053581ce9db2fa10b6f7151a54",
      "created_at": "2026-10-14 12:15:50",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_single_screen_layout_3203f8ec",
      "stage": "backend",
      "outcome": "succeeded",
      "scope_hash": "f22b66e560abba84df7db15ed11851eda93aa01c145496bea146dccc1c8b2d3c",
      "created_at": "2026-10-14 12:16:01",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_single_screen_layout_3203f8ec",
      "stage": "screens",
      "outcome": "succeeded",
      "scope_hash": "0068dc9f1ae726d17d8c3e9c5318e4cbfc6337737d7475183017cf2817b8ed26",
      "created_at": "2026-10-14 12:16:22",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_inline_error_messages_9ddfedf0",
      "stage": "database",
      "outcome": "succeeded",
      "scope_hash": "570878f318efd780897f77222f7442468c33b2053581ce9db2fa10b6f7151a54",
      "created_at": "2026-10-14 12:16:37",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_inline_error_messages_9ddfedf0",
      "stage": "backend",
      "outcome": "succeeded",
      "scope_hash": "8cdb45544a2d96b15f1cf54f10629154e586a258c63165b5fb1f83b654b3f8df",
      "created_at": "2026-10-14 12:16:51",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    },
    {
      "feature_id": "capability_inline_error_messages_9ddfedf0",
      "stage": "screens",
      "outcome": "succeeded",
      "scope_hash": "0068dc9f1ae726d17d8c3e9c5318e4cbfc6337737d7475183017cf2817b8ed26",
      "created_at": "2026-10-14 12:17:10",
      "last_error_code": null,
      "attempts": [
        {
          "code": null,
          "status": "accepted",
          "attempt": 1,
          "retryable": null,
          "detail_categories": []
        }
      ]
    }
  ]
}
```

Use feature IDs and the recorded validation details to compare tables, functions and screens. A rejected candidate is not the finalized blueprint. Missing historical details cannot be recovered.
