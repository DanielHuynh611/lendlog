-- Optional API storage; the visible MVP keeps its loans only in the browser.
-- Use a fresh database. This is not a migration for the original three tables.
CREATE TABLE IF NOT EXISTS loan_records (
  id CHAR(36) NOT NULL PRIMARY KEY,
  browser_id CHAR(36) NOT NULL,
  item_name VARCHAR(100) NOT NULL,
  borrower_name VARCHAR(100) NOT NULL,
  created_at DATETIME NOT NULL,
  CONSTRAINT ck_loan_item CHECK (CHAR_LENGTH(TRIM(item_name)) BETWEEN 1 AND 100),
  CONSTRAINT ck_loan_borrower CHECK (CHAR_LENGTH(TRIM(borrower_name)) BETWEEN 1 AND 100),
  INDEX ix_loan_browser_created (browser_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
