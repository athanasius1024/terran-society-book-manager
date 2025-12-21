# PostgreSQL Database Setup Complete!

## Database Information

**Database Name:** `terran_society`  
**Host:** localhost  
**Port:** 5432 (default)

## User Accounts

### 1. dba (Superuser)
- **Username:** dba
- **Password:** sql
- **Privileges:** Full superuser access
- **Purpose:** Database administration and maintenance

### 2. rock (Administrator)
- **Username:** rock
- **Password:** river
- **Privileges:** Full access to all Terran Society objects (OWNER)
- **Purpose:** Primary user for application and data management

### 3. overlook (Read-Only)
- **Username:** overlook
- **Password:** river
- **Privileges:** SELECT only on all tables
- **Purpose:** Read-only access for reporting and queries

## Connection Examples

### Command Line (psql)
```bash
# Connect as rock (administrator)
PGPASSWORD=river psql -h localhost -U rock -d terran_society

# Connect as overlook (read-only)
PGPASSWORD=overlook psql -h localhost -U overlook -d terran_society

# Or create .pgpass file in your home directory for passwordless access
echo "localhost:5432:terran_society:rock:river" >> ~/.pgpass
chmod 600 ~/.pgpass
psql -h localhost -U rock -d terran_society
```

### Python (psycopg2)
```python
import psycopg2

# Administrator connection
conn = psycopg2.connect(
    host="localhost",
    database="terran_society",
    user="rock",
    password="river"
)

# Read-only connection
conn_ro = psycopg2.connect(
    host="localhost",
    database="terran_society",
    user="overlook",
    password="river"
)
```

### Connection String (DATABASE_URL)
```
# Administrator
postgresql://rock:river@localhost:5432/terran_society

# Read-only
postgresql://overlook:river@localhost:5432/terran_society
```

## Schema Organization

The database is organized into 4 schemas:

### 1. ts_data (Core Organizational Data)
**16 Tables:**
- `meta` - Database metadata
- `tier`, `tier_explain` - Organizational tiers (District, Region, World)
- `branch`, `branch_explain` - Branches (Executive, Legislative, Judicial, Fair Witness, Military)
- `institution`, `institution_dtl`, `institution_explain` - Specific institutions
- `role`, `role_duty`, `role_explain` - Roles and responsibilities
- `process`, `process_dtl`, `process_explain`, `process_institution` - Processes and procedures
- `glossary` - Terms and definitions

**3 Views:**
- `v_role_full` - Complete role hierarchy
- `v_institution_full` - Complete institution information
- `v_process_full` - Processes with linked institutions

### 2. ts_books (Book Versioning)
**5 Tables:**
- `book_version` - Book versions with approval workflow
- `book_chapter` - Chapter information
- `book_section` - Section content (text, markdown, HTML)
- `book_data_ref` - Links sections to database entities
- `generated_document` - Generated files (ODT, HTML, PDF, etc.)

**1 View:**
- `v_book_summary` - Book versions with statistics

**Book Versioning Workflow:**
1. Create version: `draft` status
2. Add chapters and sections
3. Change to `review` status
4. Approve: `approved` status with approval timestamp
5. Publish: `published` status with publication timestamp
6. Archive old versions: `archived` status

### 3. ts_app (Application Metadata)
**3 Tables:**
- `setting` - Application configuration
- `user_session` - Web app sessions
- `activity_log` - User activity tracking

### 4. ts_audit (Audit Trail)
**1 Table:**
- `data_audit` - Complete audit trail of all changes

## Key Features

### 1. Timestamps
- All major tables have `created_at` and `modified_at` timestamps
- `modified_at` automatically updated via triggers
- Timezone-aware timestamps (TIMESTAMP WITH TIME ZONE)

### 2. Full-Text Search
- `pg_trgm` extension enabled for fuzzy text searching
- GIN indexes on glossary terms and section content
- Example query:
  ```sql
  SELECT * FROM ts_data.glossary 
  WHERE term % 'arbitration' 
  ORDER BY similarity(term, 'arbitration') DESC;
  ```

### 3. JSON Support
- JSONB columns for flexible metadata
- Used in book_version.metadata and activity_log.details
- Efficient indexing and querying

### 4. Provenance Tracking
- `doc_loc` field tracks source documents
- `is_example` boolean flag for example data
- `example_note` explains example purposes

### 5. Referential Integrity
- All foreign keys enforce relationships
- CASCADE deletes maintain consistency
- CHECK constraints validate enumerations

## Common Queries

### View All Tiers
```sql
SELECT * FROM ts_data.tier ORDER BY sort_order;
```

### View All Roles with Institution and Tier
```sql
SELECT * FROM ts_data.v_role_full;
```

### View Latest Book Version
```sql
SELECT * FROM ts_books.v_book_summary ORDER BY created_at DESC LIMIT 1;
```

### Search Glossary
```sql
SELECT term, short_def FROM ts_data.glossary WHERE term ILIKE '%admin%';
```

### View Audit Trail
```sql
SELECT * FROM ts_audit.data_audit 
WHERE user_name = 'rock' 
ORDER BY audit_timestamp DESC 
LIMIT 10;
```

## Data Migration

### Step 1: Migrate from SQLite
```bash
# Create and run migration script
python scripts/migrate_to_postgres.py
```

This will copy all data from `db/terran_society.db` (SQLite) to PostgreSQL.

### Step 2: Verify Migration
```bash
# Check row counts
PGPASSWORD=river psql -h localhost -U rock -d terran_society -c "
SELECT 'tier' as table, COUNT(*) FROM ts_data.tier UNION ALL
SELECT 'branch', COUNT(*) FROM ts_data.branch UNION ALL
SELECT 'institution', COUNT(*) FROM ts_data.institution UNION ALL
SELECT 'role', COUNT(*) FROM ts_data.role UNION ALL
SELECT 'role_duty', COUNT(*) FROM ts_data.role_duty;
"
```

## Book Generation from Database

### Create a New Book Version
```sql
-- Insert new version
INSERT INTO ts_books.book_version (version_number, version_name, created_by, status)
VALUES ('1.0', 'First Edition', 'rock', 'draft')
RETURNING version_id;

-- Add chapters (use the returned version_id)
INSERT INTO ts_books.book_chapter (version_id, chapter_number, chapter_title, chapter_type, sort_order)
VALUES 
    (1, 1, 'Introduction', 'introduction', 1),
    (1, 2, 'Basic Principles', 'principles', 2),
    (1, 3, 'Rights of the People', 'rights', 3);
```

### Generate Book from Database
Python script coming next will:
1. Query all organizational data
2. Generate chapters and sections
3. Create markdown, HTML, and ODT versions
4. Store generated files in ts_books.generated_document

## Backup and Restore

### Backup
```bash
# Full database backup
pg_dump -h localhost -U rock -d terran_society -F c -f terran_society_backup.dump

# Schema only
pg_dump -h localhost -U rock -d terran_society --schema-only -f schema_backup.sql

# Data only
pg_dump -h localhost -U rock -d terran_society --data-only -f data_backup.sql
```

### Restore
```bash
# Full restore
pg_restore -h localhost -U rock -d terran_society -c terran_society_backup.dump

# From SQL file
psql -h localhost -U rock -d terran_society -f backup.sql
```

## Performance Tips

1. **Analyze tables regularly:**
   ```sql
   ANALYZE;
   ```

2. **Check index usage:**
   ```sql
   SELECT schemaname, tablename, indexname, idx_scan 
   FROM pg_stat_user_indexes 
   ORDER BY idx_scan;
   ```

3. **Vacuum regularly:**
   ```sql
   VACUUM ANALYZE;
   ```

## Web Application Integration

### Flask Example
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rock:river@localhost:5432/terran_society'
db = SQLAlchemy(app)
```

### Django settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'terran_society',
        'USER': 'rock',
        'PASSWORD': 'river',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Security Notes

1. **Change passwords in production!** The current passwords are development defaults.

2. **Use SSL connections** in production:
   ```python
   conn = psycopg2.connect(
       host="localhost",
       database="terran_society",
       user="rock",
       password="river",
       sslmode='require'
   )
   ```

3. **Limit network access** via pg_hba.conf

4. **Regular backups** are essential

5. **Audit trail** captures all data changes for security review

## Next Steps

1. ✅ Database and users created
2. ✅ Schema with book versioning created
3. ⏳ Migrate data from SQLite
4. ⏳ Create Python app for book generation
5. ⏳ Create web interface
6. ⏳ Add remaining World-level roles
7. ⏳ Populate processes table
8. ⏳ Generate complete book from database

## Support

For PostgreSQL documentation: https://www.postgresql.org/docs/

Database location: `localhost:5432/terran_society`  
Admin user: `rock` / `river`  
Read-only user: `overlook` / `river`

All tables owned by: `rock`
