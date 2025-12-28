#!/usr/bin/env python3
"""
Populate ts_books.book_section from the generated manuscript.
"""

import psycopg2
from pathlib import Path

# PostgreSQL connection settings
PG_HOST = 'localhost'
PG_DATABASE = 'terran_society'
PG_USER = 'rock'
PG_PASSWORD = 'river'

MANUSCRIPT_PATH = Path(__file__).parent.parent / 'book' / 'manuscript.md'

# Map chapter titles to chapter IDs (version 1.1)
CHAPTER_MAPPING = {
    'Introduction': 11,
    'Basic Principles of Terran Society': 12,
    'Rights of the People': 13,
    'Organizational Structure Overview': 14,
    'District Level Governance': 15,
    'The Fair Witness Branch': 16,
    'Processes and Procedures': 17,
    'Glossary': 18
}

def get_connection():
    return psycopg2.connect(
        host=PG_HOST,
        database=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )

def parse_manuscript():
    """Parse manuscript into chapters and sections"""
    with open(MANUSCRIPT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chapters = {}
    current_chapter = None
    current_section = None
    current_content = []
    section_number = 0
    
    lines = content.split('\n')
    
    for line in lines:
        # Main title (skip)
        if line.startswith('# '):
            continue
        
        # Chapter headings (##)
        elif line.startswith('## '):
            # Save previous section
            if current_chapter and current_section:
                if current_chapter not in chapters:
                    chapters[current_chapter] = []
                chapters[current_chapter].append({
                    'section_number': section_number,
                    'title': current_section,
                    'content': '\n'.join(current_content).strip()
                })
            
            # Start new chapter
            current_chapter = line[3:].strip()
            current_section = None
            current_content = []
            section_number = 0
            
        # Section headings (###)
        elif line.startswith('### '):
            # Save previous section
            if current_chapter and current_section:
                if current_chapter not in chapters:
                    chapters[current_chapter] = []
                chapters[current_chapter].append({
                    'section_number': section_number,
                    'title': current_section,
                    'content': '\n'.join(current_content).strip()
                })
            
            # Start new section
            section_number += 1
            current_section = line[4:].strip()
            current_content = []
            
        # Content
        else:
            current_content.append(line)
    
    # Save final section
    if current_chapter and current_section:
        if current_chapter not in chapters:
            chapters[current_chapter] = []
        chapters[current_chapter].append({
            'section_number': section_number,
            'title': current_section,
            'content': '\n'.join(current_content).strip()
        })
    # Handle chapters with no subsections (like introduction text before first ###)
    elif current_chapter and current_content:
        if current_chapter not in chapters:
            chapters[current_chapter] = []
        chapters[current_chapter].append({
            'section_number': 1,
            'title': current_chapter,
            'content': '\n'.join(current_content).strip()
        })
    
    return chapters

def insert_sections(conn, chapters):
    """Insert book sections into database"""
    cur = conn.cursor()
    
    total_sections = 0
    for chapter_title, sections in chapters.items():
        chapter_id = CHAPTER_MAPPING.get(chapter_title)
        
        if not chapter_id:
            print(f"  Skipping unknown chapter: {chapter_title}")
            continue
        
        print(f"\nChapter: {chapter_title} (ID: {chapter_id})")
        
        for idx, section in enumerate(sections, 1):
            try:
                cur.execute("""
                    INSERT INTO ts_books.book_section 
                    (chapter_id, section_number, section_title, content_text, content_markdown, sort_order)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING section_id
                """, (
                    chapter_id,
                    str(section['section_number']),
                    section['title'],
                    section['content'],  # text version
                    section['content'],  # markdown version
                    idx  # sort_order
                ))
                section_id = cur.fetchone()[0]
                print(f"  ✓ Section {section['section_number']}: {section['title'][:50]}... (ID: {section_id})")
                total_sections += 1
            except Exception as e:
                print(f"  ✗ Error inserting section '{section['title'][:30]}': {e}")
                conn.rollback()  # Rollback on error
                raise
    
    conn.commit()
    return total_sections

def main():
    print("=" * 80)
    print("Populating ts_books.book_section from manuscript")
    print("=" * 80)
    
    # Parse manuscript
    print("\nParsing manuscript...")
    chapters = parse_manuscript()
    print(f"✓ Found {len(chapters)} chapters")
    
    # Insert into database
    print("\nInserting sections...")
    conn = get_connection()
    try:
        total = insert_sections(conn, chapters)
        print("\n" + "=" * 80)
        print(f"✓ Successfully inserted {total} sections")
        print("=" * 80)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
