# Database design

The Oracle schema is the central part of this project. Its source is preserved in `database` and is complemented by the ER diagram and table-description workbook in `docs/database`.

## Core records

- `GUARDIAN` stores parent, guardian, and staff contact information.
- `STUDENT` stores student identity and academic details.
- `COURSE` defines the available curriculum.
- `CLASS` represents class sections and their assigned courses.
- `CHALLAN` records generated fee challans.
- `ACCOMPANY` models the people authorized to accompany a student.
- `REGISTERED` connects students to classes and courses.

Log tables retain changes to important records for reporting and audit workflows.

## Database behavior

The scripts demonstrate more than table creation. They include:

- sequences for generated identifiers;
- triggers for keys, history records, and registration workflows;
- stored queries and reporting views;
- seed data used by the original system.

Run `database/schema.sql` first to create and populate the schema. `database/stored-queries.sql` contains the reporting queries and views used by the application.

## Web integration

The PHP pages access Oracle through OCI8. `web/database.php` owns the connection setup and reads its values from `ORACLE_DB_USER`, `ORACLE_DB_PASSWORD`, and `ORACLE_DB_DSN`. Credentials are deliberately kept out of source control.
