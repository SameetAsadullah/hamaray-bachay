#!/usr/bin/env python3
"""Validate the documented structure and credential hygiene."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "src/frontend web"
SQL = ROOT / "src/db scripts"


def validate_readme_images() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    targets = re.findall(r"!\[[^]]*\]\(([^)]+)\)", readme)
    local = [target for target in targets if not target.startswith(("http://", "https://"))]
    missing = [target for target in local if not (ROOT / target).is_file()]
    if missing:
        raise SystemExit(f"Missing README images: {', '.join(missing)}")


def validate_database_configuration() -> None:
    php_files = sorted(WEB.glob("*.php"))
    connection_calls = []
    forbidden = []
    for path in php_files:
        source = path.read_text(encoding="utf-8", errors="replace")
        if "oci_connect(" in source:
            connection_calls.append(path.name)
        if re.search(r"\$db_pass\s*=\s*['\"]", source):
            forbidden.append(path.name)

    if connection_calls != ["database.php"]:
        raise SystemExit(f"OCI connections must be centralized: {connection_calls}")
    if forbidden:
        raise SystemExit(f"Hardcoded database passwords found in: {forbidden}")


def main() -> None:
    required = [
        ROOT / "LICENSE",
        ROOT / ".env.example",
        WEB / "database.php",
        SQL / "DDL and DML.sql",
        SQL / "All Stored Queries.SQL",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing required files: {', '.join(missing)}")

    validate_readme_images()
    validate_database_configuration()
    php_count = len(list(WEB.glob("*.php")))
    sql_count = len(list(SQL.glob("*.sql"))) + len(list(SQL.glob("*.SQL")))
    print(f"Validated {php_count} PHP pages and {sql_count} SQL scripts.")


if __name__ == "__main__":
    main()
