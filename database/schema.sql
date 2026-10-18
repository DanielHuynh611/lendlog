-- Account-enabled LendLog schema. Existing legacy loan_records tables are untouched.
CREATE TABLE IF NOT EXISTS lendlog_users (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  email VARCHAR(254) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE IF NOT EXISTS lendlog_loans (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  item_name VARCHAR(100) NOT NULL,
  borrower_name VARCHAR(100) NOT NULL,
  created_at DATETIME NOT NULL,
  status VARCHAR(16) NOT NULL DEFAULT 'active',
  returned_at DATETIME NULL,
  CONSTRAINT fk_lendlog_user FOREIGN KEY (user_id) REFERENCES lendlog_users(id),
  CONSTRAINT ck_lendlog_loans_item CHECK (CHAR_LENGTH(TRIM(item_name)) BETWEEN 1 AND 100),
  CONSTRAINT ck_lendlog_loans_borrower CHECK (CHAR_LENGTH(TRIM(borrower_name)) BETWEEN 1 AND 100),
  CONSTRAINT ck_lendlog_loans_status CHECK (status IN ('active', 'returned')),
  CONSTRAINT ck_lendlog_loans_return_date CHECK (
    (status = 'active' AND returned_at IS NULL)
    OR (status = 'returned' AND returned_at IS NOT NULL)
  ),
  INDEX ix_lendlog_user_status_created (user_id, status, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
