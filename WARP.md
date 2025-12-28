# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a documentation and database project for the Terran Society framework. It combines SQLite/PostgreSQL databases with Python scripts to generate a structured book manuscript about organizational governance.

**Key Components:**
- **Dual Database Architecture**: SQLite (original) at `db/terran_society.db` and PostgreSQL (target) with schemas `ts_data`, `ts_books`, `ts_app`, `ts_audit`
- **Book Generation Pipeline**: Python scripts query the database and source documents to generate Markdown manuscripts
- **Document Conversion**: Pandoc converts Markdown to ODT (LibreOffice) format
- **Structured Data**: Organizational hierarchy (Tiers → Branches → Institutions → Roles → Duties) with full provenance tracking

## Database Architecture

### PostgreSQL Connection (Primary Target)
```bash
# Database: db_kirby (or terran_society)
# Schema: scm_kirby (or ts_data, ts_books, ts_app, ts_audit)
# User: rock
# Password: river (development only - use environment variables in production)
```

**Connection via psql:**
```bash
PGPASSWORD=river psql -h localhost -U rock -d db_kirby
```

**Connection in Python:**
```python
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="db_kirby",
    user="rock",
    password="river"
)
```

### Schema Structure

**PostgreSQL has 4 schemas:**
- `ts_data`: Core organizational data (tiers, branches, institutions, roles, duties)
- `ts_books`: Book versioning and content (chapters, sections, references)
- `ts_app`: Application metadata (settings, sessions, logs)
- `ts_audit`: Audit trail for all changes

**SQLite structure** (legacy, being migrated):
- Single database with tables prefixed by `t` (e.g., `tTier`, `tBranch`, `tInstitution`)
- Views prefixed by `v` (e.g., `vRoleFull`, `vInstitutionFull`)

### Key Schema Conventions
- **Provenance tracking**: `doc_loc` field tracks source document locations (e.g., "trifold-basic-rights:7", "NewShape:517-620")
- **Example data**: `is_example` boolean flag distinguishes real structure from illustrative examples
- **Timestamps**: All major tables have `created_at` and `modified_at` with automatic triggers
- **Foreign keys**: Strict referential integrity enforced throughout

## Common Development Commands

### Database Operations

**Initialize PostgreSQL database:**
```bash
# Create database and users
psql -U postgres -f scripts/pg_setup.sql

# Create schema
PGPASSWORD=river psql -h localhost -U rock -d terran_society -f scripts/pg_schema.sql
```

**Migrate from SQLite to PostgreSQL:**
```bash
python3 scripts/migrate_to_postgres.py
```

**Populate SQLite database (legacy):**
```bash
# Create schema
sqlite3 db/terran_society.db < scripts/schema.sql

# Populate base data (tiers, branches, institutions)
python3 scripts/populate_db.py

# Populate roles and duties
python3 scripts/populate_roles.py
```

**Query database directly:**
```bash
# SQLite
sqlite3 db/terran_society.db "SELECT * FROM tTier ORDER BY SortOrder;"

# PostgreSQL
PGPASSWORD=river psql -h localhost -U rock -d db_kirby -c "SELECT * FROM scm_kirby.organizations;"
```

### Book Generation

**Generate book manuscript:**
```bash
# Generates book/manuscript.md from database and source files
python3 scripts/generate_book.py
```

**Convert Markdown to ODT:**
```bash
# Requires pandoc to be installed
pandoc book/manuscript.md -o book/TerranSocietyBook.odt --toc --toc-depth=3
```

**Full build pipeline:**
```bash
# SQLite workflow (original)
sqlite3 db/terran_society.db < scripts/schema.sql
python3 scripts/populate_db.py
python3 scripts/populate_roles.py
python3 scripts/generate_book.py
pandoc book/manuscript.md -o book/TerranSocietyBook.odt --toc --toc-depth=3
```

### Python Environment

**No requirements.txt file exists** - dependencies are minimal:
- `sqlite3` (built-in)
- `psycopg2` or `psycopg2-binary` (for PostgreSQL)
- Standard library only for most scripts

**Install PostgreSQL adapter if needed:**
```bash
pip3 install psycopg2-binary
```

**Python version:** Python 3.13.5 (or compatible 3.x)

## Architecture Notes

### Data Flow
1. **Source Documents** (`inputs/` directory) → Provide raw content about Terran Society
2. **Python Scripts** (`scripts/`) → Parse sources and populate database
3. **Database** (`db/`) → Stores structured organizational data
4. **Generation Script** (`scripts/generate_book.py`) → Queries database and formats as Markdown
5. **Pandoc** → Converts Markdown to ODT for final document

### Key Design Patterns
- **Database-driven documentation**: Book content is generated from structured data, not maintained as static text
- **Provenance tracking**: Every piece of data tracks its source document via `doc_loc` field
- **Hierarchical organization**: Tier (District/Region/World) → Branch (Executive/Legislative/Judicial/Fair Witness/Military) → Institution → Role → Duty
- **Version control**: PostgreSQL schema includes book versioning with approval workflow (`draft` → `review` → `approved` → `published`)

### File Organization
```
.
├── book/              # Generated book manuscripts and outputs
├── config/            # Database configuration files
│   ├── database.ini   # PostgreSQL connection settings
│   └── .env.template  # Environment variable template
├── db/                # Database files
│   ├── terran_society.db  # SQLite database
│   └── schema.sql     # Basic PostgreSQL schema (newer version in scripts/)
├── docs/              # Additional documentation
├── inputs/            # Source documents for content
├── reference/         # Reference materials
├── scripts/           # Database and generation scripts
│   ├── schema.sql           # SQLite schema
│   ├── pg_setup.sql         # PostgreSQL initial setup
│   ├── pg_schema.sql        # PostgreSQL full schema
│   ├── populate_db.py       # Populate tiers/branches/institutions
│   ├── populate_roles.py    # Populate roles and duties
│   ├── generate_book.py     # Generate book manuscript
│   └── migrate_to_postgres.py  # Migrate SQLite → PostgreSQL
└── src/               # Empty (future application code)
```

## Database Connection Priority

When writing new code that needs database access:

1. **Prefer PostgreSQL** (db_kirby/scm_kirby) for new development
2. Use **SQLite** (db/terran_society.db) only for legacy compatibility or when explicitly requested
3. Connection details:
   - Host: localhost
   - Database: db_kirby (or terran_society for full PostgreSQL schema)
   - Schema: scm_kirby (or ts_data, ts_books, ts_app, ts_audit)
   - User: rock
   - Password: Use environment variable `DB_PASSWORD` or read from config/database.ini

## Important Notes

- **Passwords in config files**: The password "river" appears in multiple files - this is for development only. Never commit production credentials.
- **Two database systems**: Project is transitioning from SQLite to PostgreSQL. Check which system scripts expect before running them.
- **Schema naming**: SQLite uses `tTableName` convention; PostgreSQL uses `schema.table_name` convention
- **Document conversion**: Pandoc must be installed system-wide (`/usr/bin/pandoc`) for ODT generation
- **Provenance format**: Source references use format "document-name:line-numbers" (e.g., "NewShape:517-620")
- **Virtual environment**: A `.venv/` directory exists but appears incomplete - scripts generally use system Python

## Testing and Verification

**Verify database contents:**
```bash
# Check row counts in SQLite
sqlite3 db/terran_society.db "SELECT 'Tiers' as table, COUNT(*) as count FROM tTier
UNION SELECT 'Branches', COUNT(*) FROM tBranch
UNION SELECT 'Institutions', COUNT(*) FROM tInstitution
UNION SELECT 'Roles', COUNT(*) FROM tRole
UNION SELECT 'Duties', COUNT(*) FROM tRole_Duty;"

# Check PostgreSQL migration success
PGPASSWORD=river psql -h localhost -U rock -d terran_society -c "
SELECT 'tier' as table, COUNT(*) FROM ts_data.tier UNION ALL
SELECT 'branch', COUNT(*) FROM ts_data.branch UNION ALL
SELECT 'institution', COUNT(*) FROM ts_data.institution UNION ALL
SELECT 'role', COUNT(*) FROM ts_data.role UNION ALL
SELECT 'role_duty', COUNT(*) FROM ts_data.role_duty;"
```

## Current Project Status

According to STATUS.md:
- SQLite database is populated with 3 tiers, 5 branches, 28 institutions, 37 roles, 73 duties
- District level chapter complete
- Regional and World level chapters in progress
- Migration to PostgreSQL underway
- Book generation pipeline functional

See STATUS.md for detailed progress tracking.
