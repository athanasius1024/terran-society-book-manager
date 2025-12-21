#!/usr/bin/env python3
"""
Populate the Terran Society database with organizational structure data.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'db' / 'terran_society.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def populate_tiers(conn):
    """Insert the three tiers"""
    tiers = [
        ('District', 'DIST', 1, 'trifold-basic-rights:7'),
        ('Region', 'REGN', 2, 'trifold-basic-rights:8'),
        ('World', 'WRLD', 3, 'trifold-basic-rights:9'),
    ]
    
    conn.executemany('''
        INSERT OR IGNORE INTO tTier (TierName, TierCode, SortOrder, DocLoc)
        VALUES (?, ?, ?, ?)
    ''', tiers)
    
    tier_explain = [
        ('District', 'Foundation of Representation', 
         'The District is the most local tier of Terran Society, composed of a Council of Elders '
         'and a Representative to the Regional Legislature. Districts typically range from 5,000 to 21,000 people, '
         'providing a human-scale community where residents are likely to personally know at least one Elder.',
         'trifold-basic-rights:7', 1),
        ('Region', 'Primary Governance Structure',
         'The Region is the primary governance tier, with full executive, legislative, judicial, and Fair Witness branches. '
         'Regional boundaries are set to not exceed 20-25 million people, ensuring responsive and accountable governance. '
         'Each Region manages its own public services, resources, and administration.',
         'trifold-basic-rights:8', 1),
        ('World', 'Planetary Coordination',
         'The World tier provides planetary-level coordination for matters that cross regional boundaries, including '
         'defense, inter-regional commerce, environmental standards, and the Fair Witness system. '
         'It ensures equal treatment of all Regions and coordination of global challenges.',
         'trifold-basic-rights:9', 1),
    ]
    
    conn.executemany('''
        INSERT OR IGNORE INTO tTierExplain (TierName, TierExplainHeader, TierExplainDesc, DocLoc, SortOrder)
        VALUES (?, ?, ?, ?, ?)
    ''', tier_explain)

def populate_branches(conn):
    """Insert the branches"""
    branches = [
        ('Executive', 'EXEC', 'Executive Branch', 
         'Administers daily operations, public services, and implementation of legislation', 
         1, 'trifold-basic-rights:8'),
        ('Legislative', 'LEGIS', 'Legislative Branch',
         'Creates laws, approves budgets, and provides oversight of other branches',
         2, 'trifold-basic-rights:8'),
        ('Judicial', 'JUDIC', 'Judicial Branch',
         'Provides dispute resolution, rights protection, and justice through courts',
         3, 'NewShape:517-620'),
        ('Fair Witness', 'FAIRW', 'Fair Witness Branch',
         'Independent record-keeping, observation, and transparency oversight',
         4, 'NewShape:718-772'),
        ('Military', 'MILIT', 'Military and Intelligence',
         'Planetary defense and intelligence gathering under civilian oversight',
         5, 'NewShape:773-836'),
    ]
    
    conn.executemany('''
        INSERT OR IGNORE INTO tBranch (BranchName, BranchCode, BranchHeader, BranchDesc, SortOrder, DocLoc)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', branches)

def populate_district_institutions(conn):
    """Insert District-level institutions"""
    institutions = [
        ('Council of Elders', 'District', 'Legislative', 
         'Council of Elders',
         'Primary governance body at the District level, focused on family welfare, dispute resolution, and community cohesion',
         'council-of-elders:1-40', 1),
    ]
    
    cur = conn.cursor()
    for name, tier, branch, header, desc, docloc, sort in institutions:
        cur.execute('''
            INSERT OR IGNORE INTO tInstitution 
            (InstitutionName, TierName, BranchName, InstitutionHeader, InstitutionDesc, DocLoc, SortOrder)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, tier, branch, header, desc, docloc, sort))

def populate_regional_institutions(conn):
    """Insert Region-level institutions"""
    institutions = [
        # Executive
        ('Regional Executive Council', 'Region', 'Executive',
         'Regional Executive Council',
         'Coordinating body of the five executive departments, sharing leadership on a rotational basis',
         'NewShape:393-416', 1),
        ('Office of Regional Administrator', 'Region', 'Executive',
         'Office of Regional Administrator',
         'Manages regional government operations, facilities, staffing, elections, and public service infrastructure',
         'NewShape:418-441', 2),
        ('Office of Regional Treasurer', 'Region', 'Executive',
         'Office of Regional Treasurer',
         'Manages regional budget, taxation, benefits accounts, audits, and financial oversight',
         'NewShape:443-458', 3),
        ('Office of Regional Ambassador', 'Region', 'Executive',
         'Office of Regional Ambassador',
         'Promotes commerce, tourism, economic development, and assists regional members traveling in other Regions',
         'NewShape:460-469', 4),
        ('Office of Regional Sheriff', 'Region', 'Executive',
         'Office of Regional Sheriff',
         'Protects Rights of the People, conducts investigations, maintains public safety, and emergency response',
         'NewShape:471-486', 5),
        ('Office of Regional Environmental Guardian', 'Region', 'Executive',
         'Office of Regional Environmental Guardian',
         'Environmental protection, pollution monitoring, ecosystem restoration, and enforcement of environmental standards',
         'NewShape:488-514', 6),
        
        # Legislative
        ('Regional Council of the People', 'Region', 'Legislative',
         'Regional Council of the People',
         'Representative legislative body with one seat per District, passes laws, approves budgets, charters cooperatives',
         'NewShape:346-376', 1),
        
        # Judicial
        ('Office of Guarantor of Rights', 'Region', 'Judicial',
         'Office of Guarantor of Rights',
         'Investigates rights violations, presents cases to Warrant Jury, watches over Sheriff and Executive officials',
         'NewShape:646-653', 1),
        ('Office of Facilitator of the Court', 'Region', 'Judicial',
         'Office of Facilitator of the Court (Conductor)',
         'Presides over Major and Minor Courts, manages court process, advises jury, ensures procedural fairness',
         'NewShape:629-644', 2),
        ('Office of Public Arbitrator', 'Region', 'Judicial',
         'Office of Public Arbitrator',
         'Provides voluntary arbitration services for dispute resolution outside formal court system',
         'NewShape:655-666', 3),
        ('Regional Minor Court', 'Region', 'Judicial',
         'Regional Minor Court',
         'Handles petty criminal cases with 7-person jury (6-of-7 verdict required)',
         'NewShape:532-543', 4),
        ('Regional Major Court', 'Region', 'Judicial',
         'Regional Major Court',
         'Handles serious criminal cases with 14-person jury (12-of-14 verdict required)',
         'NewShape:532-543', 5),
        ('Regional Arbitration Court', 'Region', 'Judicial',
         'Regional Arbitration Court',
         'Voluntary dispute resolution forum with binding arbitration',
         'NewShape:549-560', 6),
        
        # Fair Witness
        ('Regional Fair Witness Council', 'Region', 'Fair Witness',
         'Regional Fair Witness Council',
         'Nine-member elected council managing Fair Witness operations, training, and certification in the Region',
         'NewShape:764', 1),
        ('Fair Witness Training Academy', 'Region', 'Fair Witness',
         'Fair Witness Training and Certification',
         'Rigorous training program for observation skills, memorization, recall, documentation, and ethical standards',
         'NewShape:749-761', 2),
    ]
    
    cur = conn.cursor()
    for name, tier, branch, header, desc, docloc, sort in institutions:
        cur.execute('''
            INSERT OR IGNORE INTO tInstitution 
            (InstitutionName, TierName, BranchName, InstitutionHeader, InstitutionDesc, DocLoc, SortOrder)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, tier, branch, header, desc, docloc, sort))

def populate_world_institutions(conn):
    """Insert World-level institutions"""
    institutions = [
        # Executive
        ('Planetary Executive Council', 'World', 'Executive',
         'Planetary Executive Council',
         'Five-member council coordinating planetary-level executive functions with rotational leadership',
         'NewShape:690-716', 1),
        ('Office of Planetary Administrator', 'World', 'Executive',
         'Office of Planetary Administrator',
         'Coordinates standards, best practices, and inter-regional administrative matters',
         'NewShape:680', 2),
        ('Office of Planetary Treasurer', 'World', 'Executive',
         'Office of Planetary Treasurer',
         'Manages planetary currency, coordinates regional financial systems, oversees planetary budget',
         'NewShape:682', 3),
        ('Office of Planetary Ambassador', 'World', 'Executive',
         'Office of Planetary Ambassador',
         'Manages relations with external entities and coordinates inter-regional diplomatic efforts',
         'NewShape:686', 4),
        ('Office of Planetary Sheriff', 'World', 'Executive',
         'Office of Planetary Sheriff',
         'Coordinates inter-regional law enforcement, assists with crimes spanning multiple Regions',
         'NewShape:684', 5),
        ('Office of Planetary Environmental Guardian', 'World', 'Executive',
         'Office of Planetary Environmental Guardian',
         'Coordinates global environmental monitoring, sets planetary environmental standards',
         'NewShape:688', 6),
        
        # Legislative
        ('Planetary Council of the People', 'World', 'Legislative',
         'Planetary Council of the People',
         'Population-based legislative body representing all members of Terran Society',
         'NewShape:673', 1),
        ('Council of the Regions', 'World', 'Legislative',
         'Council of the Regions',
         'Legislative body with equal representation from each Region',
         'NewShape:673', 2),
        
        # Fair Witness
        ('Planetary Fair Witness Council', 'World', 'Fair Witness',
         'Planetary Fair Witness Council',
         'Twenty-seven member council elected from Senior Certified Fair Witnesses for nine-year terms',
         'NewShape:768', 1),
        
        # Military
        ('Planetary Defense Force', 'World', 'Military',
         'Planetary Defense Force',
         'Unified military organization for planetary defense with minimal active duty and large reserve force',
         'NewShape:774-819', 1),
        ('Defense Force Council', 'World', 'Military',
         'Defense Force Council',
         'Nine-member council commanding the Defense Force with mixed civilian and military membership',
         'NewShape:780-788', 2),
        ('Defense Force Intelligence', 'World', 'Military',
         'Defense Force Intelligence',
         'Intelligence collection and analysis for planetary defense, subject to oversight',
         'NewShape:831-835', 3),
    ]
    
    cur = conn.cursor()
    for name, tier, branch, header, desc, docloc, sort in institutions:
        cur.execute('''
            INSERT OR IGNORE INTO tInstitution 
            (InstitutionName, TierName, BranchName, InstitutionHeader, InstitutionDesc, DocLoc, SortOrder)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, tier, branch, header, desc, docloc, sort))

def main():
    print("Populating Terran Society database...")
    conn = get_connection()
    
    try:
        populate_tiers(conn)
        print("✓ Tiers populated")
        
        populate_branches(conn)
        print("✓ Branches populated")
        
        populate_district_institutions(conn)
        print("✓ District institutions populated")
        
        populate_regional_institutions(conn)
        print("✓ Regional institutions populated")
        
        populate_world_institutions(conn)
        print("✓ World institutions populated")
        
        conn.commit()
        
        # Show summary
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tTier")
        print(f"\nDatabase populated: {cur.fetchone()[0]} tiers")
        cur.execute("SELECT COUNT(*) FROM tBranch")
        print(f"                     {cur.fetchone()[0]} branches")
        cur.execute("SELECT COUNT(*) FROM tInstitution")
        print(f"                     {cur.fetchone()[0]} institutions")
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
