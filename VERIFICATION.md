# Account-enabled application verification — 17 October 2026

- 73 automated checks passed: registration/login/logout, password hashing,
  input validation, CSRF, ownership isolation, edit/delete/return/restore, database
  restart persistence, repeatable schema setup and legacy-table preservation.
- Desktop (1440px) and mobile (390px) browser flows passed: registration,
  editing/validation/cancel, return/restore, deletion/cancel, failed-request
  recovery, reload persistence, responsive navigation and sign-out.
- Authentication screens have no sidebar. Signed-in screens expose two
  navigation items: Loans and History; sign-out remains in the sidebar.
- The original visual theme and component styling are retained.
- Browser-local data is not automatically uploaded or removed.
- Automated tests use SQLite. An additional live local MySQL smoke check passed:
  fresh SQL schema, init-db, registration/login, Unicode, edit, return/restore,
  ownership isolation, restart persistence and deletion. Only the temporary
  test database was removed afterward; existing databases were unchanged.
- EC2, DNS, TLS issuance and Linux systemd execution are not performed here.

The files in verification/ retain the original generator's historical reports.
