CREATE TABLE `f_03ab1d7c__loan_records` (
  `id` CHAR(36) NOT NULL,
  `item_name` VARCHAR(255) NOT NULL,
  `borrower_name` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `f_3af7a315__loan_records` (
  `id` CHAR(36) NOT NULL,
  `item_name` VARCHAR(255) NOT NULL,
  `borrower_name` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `f_e3bf329c__loans` (
  `id` CHAR(36) NOT NULL,
  `item_name` VARCHAR(255) NOT NULL,
  `borrower_name` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- No database tables are required for feature: capability_character_limit_validation_533aef43


-- No database tables are required for feature: capability_required_field_validation_18c05c66


-- No database tables are required for feature: capability_single_screen_layout_3203f8ec


-- No database tables are required for feature: capability_inline_error_messages_9ddfedf0