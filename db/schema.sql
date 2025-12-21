-- Terran Society Database Schema
-- Database: db_kirby
-- Schema: scm_kirby
-- User: rock

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS scm_kirby;

-- Set search path
SET search_path TO scm_kirby, public;

-- Core Tables for Terran Society Book and Database

-- Table: Organizations
-- Stores information about Terran Society organizations and structure
CREATE TABLE IF NOT EXISTS organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    description TEXT,
    established_date DATE,
    parent_org_id INTEGER REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Principles
-- Core principles and values of the Terran Society
CREATE TABLE IF NOT EXISTS principles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    full_text TEXT,
    sort_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Book Chapters
-- Structure for book content
CREATE TABLE IF NOT EXISTS book_chapters (
    id SERIAL PRIMARY KEY,
    chapter_number INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255),
    content TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    word_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Book Sections
-- Sections within chapters
CREATE TABLE IF NOT EXISTS book_sections (
    id SERIAL PRIMARY KEY,
    chapter_id INTEGER REFERENCES book_chapters(id) ON DELETE CASCADE,
    section_number INTEGER,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    sort_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: References
-- Bibliography and reference materials
CREATE TABLE IF NOT EXISTS references (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255),
    publication_date DATE,
    source_type VARCHAR(100),
    url TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Council of Elders
-- Information about the Council of Elders structure
CREATE TABLE IF NOT EXISTS council_members (
    id SERIAL PRIMARY KEY,
    role VARCHAR(100),
    description TEXT,
    responsibilities TEXT,
    term_length VARCHAR(50),
    selection_method TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Tags
-- For categorizing and organizing content
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Junction Tables

-- Chapter-Reference relationship
CREATE TABLE IF NOT EXISTS chapter_references (
    chapter_id INTEGER REFERENCES book_chapters(id) ON DELETE CASCADE,
    reference_id INTEGER REFERENCES references(id) ON DELETE CASCADE,
    PRIMARY KEY (chapter_id, reference_id)
);

-- Chapter-Tags relationship
CREATE TABLE IF NOT EXISTS chapter_tags (
    chapter_id INTEGER REFERENCES book_chapters(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (chapter_id, tag_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_organizations_parent ON organizations(parent_org_id);
CREATE INDEX IF NOT EXISTS idx_book_sections_chapter ON book_sections(chapter_id);
CREATE INDEX IF NOT EXISTS idx_book_chapters_status ON book_chapters(status);
CREATE INDEX IF NOT EXISTS idx_references_type ON references(source_type);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers to tables
CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_principles_updated_at BEFORE UPDATE ON principles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_book_chapters_updated_at BEFORE UPDATE ON book_chapters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_book_sections_updated_at BEFORE UPDATE ON book_sections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_references_updated_at BEFORE UPDATE ON references
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_council_members_updated_at BEFORE UPDATE ON council_members
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments on tables
COMMENT ON TABLE organizations IS 'Stores information about Terran Society organizations and structure';
COMMENT ON TABLE principles IS 'Core principles and values of the Terran Society';
COMMENT ON TABLE book_chapters IS 'Structure for book content chapters';
COMMENT ON TABLE book_sections IS 'Sections within book chapters';
COMMENT ON TABLE references IS 'Bibliography and reference materials';
COMMENT ON TABLE council_members IS 'Information about the Council of Elders structure';
COMMENT ON TABLE tags IS 'Tags for categorizing and organizing content';
