# Terran Society Book and Database

A comprehensive project documenting and organizing information about the Terran Society framework, including book content, database schema, and reference materials.

## Project Overview

This project combines documentation, database design, and content creation for the Terran Society initiative. It includes:

- **Book Content**: Structured chapters and content for the Terran Society book
- **Database**: PostgreSQL database schema and management for organizing Terran Society data
- **Reference Materials**: Supporting documents, presentations, and historical materials
- **Scripts**: Utilities for database management and content generation

## Project Structure

```
.
├── book/           # Book chapters and content
├── db/             # Database schema and SQL files
├── inputs/         # Source materials and inputs
├── reference/      # Reference documents and materials
├── scripts/        # Utility scripts
├── .venv/          # Python virtual environment
└── docs/           # Additional documentation
```

## Database Setup

The project uses PostgreSQL 17 for data management. See `POSTGRESQL_SETUP.md` for detailed setup instructions.

**Database Configuration:**
- Server: PostgreSQL 17
- User: rock
- Password: river
- Database: db_kirby
- Schema: scm_kirby

## Getting Started

1. **Clone or navigate to the repository**
   ```bash
   cd /media/infodine/LaCie/z_stash/z-terran/TerranSocietyBook/infobuild
   ```

2. **Activate Python virtual environment** (if needed)
   ```bash
   source .venv/bin/activate
   ```

3. **Set up the database**
   Follow instructions in `POSTGRESQL_SETUP.md`

4. **Review existing content**
   - Check `Book_outline.md` for book structure
   - Review `STATUS.md` for current project status
   - Explore the `book/` directory for content

## Documentation

- `Book_outline.md` - Outline and structure of the book
- `POSTGRESQL_SETUP.md` - Database setup and configuration
- `STATUS.md` - Current project status and progress
- `WhatisTerranSociety.pdf` - Overview document

## Development

This project uses:
- Python (virtual environment in `.venv/`)
- PostgreSQL 17
- Git for version control

## Contributing

This is a personal project for documenting and organizing Terran Society materials.

## License

Copyright © Terran Society Project
