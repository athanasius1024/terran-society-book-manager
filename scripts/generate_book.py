#!/usr/bin/env python3
"""
Generate the Terran Society book manuscript in Markdown format.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'db' / 'terran_society.db'
INPUTS_PATH = Path(__file__).parent.parent / 'inputs'
OUTPUT_PATH = Path(__file__).parent.parent / 'book' / 'manuscript.md'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_rights():
    """Load Rights of the People from source"""
    rights_file = INPUTS_PATH / 'trifold-basic-rights_2021April-reformatJul2025.txt'
    with open(rights_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract rights section
    rights_start = content.find('01 Each Person')
    rights_end = content.find('~ ~ ~ ~')
    rights_text = content[rights_start:rights_end].strip()
    
    # Parse individual rights
    rights = []
    lines = rights_text.split('\n')
    current_right = []
    current_num = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Check if starts with number
        if line[:2].isdigit():
            if current_right:
                rights.append((current_num, ' '.join(current_right)))
            current_num = line[:2]
            current_right = [line[2:].strip()]
        else:
            if current_right:
                current_right.append(line)
    
    if current_right:
        rights.append((current_num, ' '.join(current_right)))
    
    return rights

def load_principles():
    """Load Basic Principles"""
    principles = [
        ("Operations Transparency", "Terran Society operations need to be open, transparent and accessible to all members as the base of power is the informed individual."),
        ("Member-Centric Design", "Terran Society services and systems must be designed, developed and administered for the benefit of all members."),
        ("Environmental Stewardship", "We are caretakers in this wonderful world shared with many other beings, pollution of air, water and land is to be avoided and cleaned up."),
        ("Equal Regional Treatment", "Services provided to Regions must be administered equally per Region."),
        ("Sustainable Infrastructure", "Permanent structures & facilities shall be designed to last for future generations, have minimal maintenance and be as energy independent and efficient as is practical."),
        ("Regional Self-Sufficiency", "Each community and region should be self-sufficient in a sustainable way for meeting their basic needs."),
        ("Single Branch Service", "A Person may be on the staff of only one branch of World, Regional or District management or the Defense Force at a time."),
        ("Inviolable Voting Rights", "Voting rights and benefits cannot be revoked as punishment or penalty."),
    ]
    return principles

def generate_introduction():
    return """# Terran Society: A New Social Contract

## Introduction

Terran Society represents a comprehensive framework for human governance designed to protect individual rights, ensure accountability, and create sustainable prosperity. Unlike traditional governmental systems that concentrate power, Terran Society distributes authority across multiple tiers and branches with built-in checks and balances.

The foundation of this system rests on two pillars: the Rights of the People and the Basic Principles. These establish the core values that guide every aspect of Terran Society's operations. From these foundations emerges an organizational structure spanning three tiers—District, Region, and World—each with specific responsibilities and limitations.

### Core Objectives

Terran Society exists to:

1. **Protect the Rights of the People** – Every member's fundamental rights are guaranteed and actively defended
2. **Meet Basic Needs** – Ensure all members have access to clean food, water, air, shelter, safety, privacy, information, travel, and healthcare
3. **Provide Just Governance** – Create transparent, accountable systems for collective decision-making
4. **Enable Peaceful Resolution** – Establish fair processes for resolving disputes without violence
5. **Ensure Common Defense** – Protect the society and its members from external threats
6. **Foster Sustainability** – Build systems that can endure for generations while respecting the natural world

### Why a New System?

Current governmental systems worldwide share common flaws: concentrated power, lack of transparency, erosion of individual rights, and structures that serve special interests rather than the people. Terran Society addresses these systemic problems through:

- **Decentralization** – Power is distributed across regions and branches, preventing dangerous concentrations
- **Transparency** – The Fair Witness branch ensures all governmental actions are recorded and public
- **Direct Accountability** – Most major positions are directly elected by the people they serve
- **Rights-First Approach** – The Rights of the People cannot be legislated away
- **Practical Scale** – Regions are sized for responsive governance (maximum 20-25 million people)

### How to Use This Book

This book provides a comprehensive guide to Terran Society's structure and operations. It is organized to build understanding progressively:

- **Basic Principles** – The fundamental values guiding all operations
- **Rights of the People** – The complete enumeration of protected rights
- **Organizational Structure** – Detailed explanation of each tier and branch
- **Roles and Responsibilities** – Clear definitions of every position and duty
- **Processes and Procedures** – How elections, legislation, courts, and other systems operate

Throughout this book, terms appearing in the Glossary are capitalized when referring to specific offices or institutions (e.g., "Administrator" for the office, "administrator" for the general concept).

"""

def generate_principles(principles):
    md = "## Basic Principles of Terran Society\n\n"
    md += "These eight principles guide all operations and decisions within Terran Society. They serve as a philosophical foundation ensuring that systems remain focused on member welfare, transparency, and sustainability.\n\n"
    
    for i, (title, desc) in enumerate(principles, 1):
        md += f"### Principle {i}: {title}\n\n"
        md += f"{desc}\n\n"
        
        # Add elaboration
        if i == 1:
            md += "This principle recognizes that an informed citizenry is the only reliable check on governmental power. All meetings of governing bodies must be observed by Fair Witnesses, and records must be freely accessible. Secret legislation or hidden agendas cannot exist in this system.\n\n"
        elif i == 2:
            md += "Government exists to serve the people, not the other way around. Every system, service, and structure must be evaluated based on whether it benefits all members. Policies that advantage one group at the expense of others violate this principle.\n\n"
        elif i == 3:
            md += "Humans are part of a larger ecological community. Our survival depends on clean air, water, and soil. This principle establishes environmental protection not as an optional add-on, but as a core requirement. The Environmental Guardian role exists at both Regional and World levels to enforce this principle.\n\n"
        elif i == 4:
            md += "No Region should receive preferential treatment in the allocation of resources or services. This ensures fairness and prevents regional rivalry. World-level services are distributed equally per Region regardless of population, wealth, or political influence.\n\n"
        elif i == 5:
            md += "Short-term thinking creates long-term problems. Terran Society requires that infrastructure be built to last generations, minimizing the burden on future members. This principle encourages renewable energy, durable materials, and efficient design.\n\n"
        elif i == 6:
            md += "Resilience comes from local self-sufficiency. While trade and cooperation between Regions are encouraged, each Region should be capable of meeting its own basic needs. This prevents cascading failures and reduces vulnerability to disruption.\n\n"
        elif i == 7:
            md += "To prevent conflicts of interest and ensure focused service, individuals cannot simultaneously serve in multiple branches or levels of government. This also distributes leadership opportunities across more people.\n\n"
        elif i == 8:
            md += "Voting rights and membership benefits are fundamental and cannot be revoked as punishment. Even those convicted of crimes retain their voice in society. This prevents the creation of a permanent underclass and ensures that everyone maintains a stake in the system.\n\n"
    
    return md

def generate_rights(rights):
    md = "## Rights of the People\n\n"
    md += "These 31 rights form the cornerstone of Terran Society. They are in-alienable, meaning they cannot be legislated away, suspended, or revoked. Every law, every governmental action, and every institution must respect these rights.\n\n"
    md += "### Foundational Statement\n\n"
    md += "We are endowed by our Creator with certain in-alienable Rights, among these are Life, Liberty and the Pursuit of Happiness. These Rights are not to be violated by institutions, organizations or individuals. Our duty is to protect these Rights.\n\n"
    md += "### The Rights\n\n"
    
    for num, text in rights:
        md += f"#### Right {num}\n\n"
        md += f"{text}\n\n"
    
    return md

def generate_org_overview(conn):
    md = "## Organizational Structure Overview\n\n"
    md += "Terran Society is organized into three tiers, each with specific roles and responsibilities. At the Regional and World levels, these tiers are further divided into branches that provide checks and balances on each other.\n\n"
    
    md += "### The Three Tiers\n\n"
    
    cur = conn.cursor()
    cur.execute('''
        SELECT t.TierName, te.TierExplainDesc 
        FROM tTier t
        LEFT JOIN tTierExplain te ON t.TierName = te.TierName
        ORDER BY t.SortOrder
    ''')
    
    for row in cur.fetchall():
        md += f"#### {row['TierName']}\n\n"
        md += f"{row['TierExplainDesc']}\n\n"
    
    md += "### The Branches\n\n"
    md += "At the Regional and World levels, governance is organized into distinct branches, each with different responsibilities:\n\n"
    
    cur.execute('''
        SELECT BranchName, BranchDesc
        FROM tBranch
        ORDER BY SortOrder
    ''')
    
    for row in cur.fetchall():
        md += f"**{row['BranchName']} Branch**: {row['BranchDesc']}\n\n"
    
    return md

def generate_district_level(conn):
    md = "## District Level Governance\n\n"
    md += "The District is the most local tier of Terran Society, designed to be small enough that residents personally know at least one Elder. Districts typically range from 5,000 to 21,000 people.\n\n"
    
    md += "### Council of Elders\n\n"
    md += "The Council of Elders serves as the primary governance body at the District level. Its focus is on community cohesion, family welfare, and peaceful dispute resolution.\n\n"
    
    md += "#### Composition\n\n"
    md += "- Seven to nine elected Elders, depending on District population\n- Three-year terms with staggered elections (one-third up for election each year)\n- No term limits\n- Candidates must demonstrate compassion and love for children\n- Preferably at least 55 years of age\n\n"
    
    md += "#### Responsibilities\n\n"
    
    cur = conn.cursor()
    cur.execute('''
        SELECT rd.RoleDutyHeader, rd.RoleDutyDesc
        FROM tRole r
        JOIN tRoleDuty rd ON r.RoleID = rd.RoleID
        JOIN tInstitution i ON r.InstitutionID = i.InstitutionID
        WHERE i.InstitutionName = 'Council of Elders'
        AND r.RoleName = 'Elder'
        ORDER BY rd.SortOrder
    ''')
    
    for row in cur.fetchall():
        md += f"**{row['RoleDutyHeader']}**: {row['RoleDutyDesc']}\n\n"
    
    md += "#### Safe Haven\n\n"
    md += "Each Council of Elders maintains a safe haven—a secure location where children or family members in crisis can temporarily stay. This provides immediate protection while the Council works to resolve the underlying issues and restore the family unit.\n\n"
    
    md += "#### Limitations\n\n"
    md += "The Council of Elders:\n"
    md += "- Cannot tax or charge service fees (funded through Regional budget allocation)\n"
    md += "- Cannot compel anyone to appear or enforce decisions (unresolved issues escalate to Sheriff or Courts)\n"
    md += "- Serves a voluntary mediation role—parties must agree to Council involvement\n\n"
    
    md += "### District Representative\n\n"
    md += "Each District elects one Representative to the Regional Council of the People. This provides direct representation in Regional legislation and ensures District concerns are heard at the Regional level.\n\n"
    
    md += "### District Elections\n\n"
    md += "District elections occur on a three-year cycle. The Administrator's Department manages the election process, ensuring:\n\n"
    md += "- Transparent candidate disclosure\n"
    md += "- Public forums for debate and questions\n"
    md += "- Physical ballots verified by voters\n"
    md += "- Ballots counted publicly and retained for 10 years\n"
    md += "- No party affiliation required\n"
    md += "- No money in campaigns\n\n"
    
    return md

def generate_glossary(conn):
    md = "## Glossary\n\n"
    
    glossary_terms = {
        'Arbitration': 'A method of dispute resolution where parties voluntarily agree to have an Arbitrator hear their case and make a binding decision.',
        'Arbitrator': 'An elected official who conducts arbitration hearings and issues binding rulings.',
        'Cooperative': 'An organization owned and controlled by its members or workers, operating for mutual benefit rather than profit.',
        'District': 'The smallest tier of Terran Society, typically 5,000 to 21,000 people, governed by a Council of Elders.',
        'Elder': 'An elected member of a District Council of Elders.',
        'Facilitator of the Court': 'An elected official (also called Conductor) who presides over Major and Minor Courts.',
        'Fair Witness': 'An independent, certified observer who records governmental proceedings objectively.',
        'Jury': 'A group of citizens who decide the outcome of court cases.',
        'Public Service Cooperative': 'A chartered organization that provides public services like utilities, transit, or ports.',
        'Region': 'The primary governance tier, with complete executive, legislative, judicial, and Fair Witness branches. Maximum population 20-25 million.',
        'Representative': 'An elected member of the Regional Council of the People.',
        'World': 'The planetary tier coordinating matters that span regions.',
    }
    
    # Add roles from database
    cur = conn.cursor()
    cur.execute('''
        SELECT DISTINCT r.RoleName, r.RoleDesc
        FROM tRole r
        ORDER BY r.RoleName
    ''')
    
    for row in cur.fetchall():
        glossary_terms[row['RoleName']] = row['RoleDesc']
    
    # Add institutions
    cur.execute('''
        SELECT DISTINCT InstitutionName, InstitutionDesc
        FROM tInstitution
        ORDER BY InstitutionName
    ''')
    
    for row in cur.fetchall():
        if row['InstitutionName'] not in glossary_terms:
            glossary_terms[row['InstitutionName']] = row['InstitutionDesc']
    
    # Sort and output
    for term in sorted(glossary_terms.keys()):
        md += f"**{term}**: {glossary_terms[term]}\n\n"
    
    return md

def main():
    print("Generating Terran Society book manuscript...")
    
    conn = get_connection()
    
    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            # Title and introduction
            f.write(generate_introduction())
            
            # Basic Principles
            principles = load_principles()
            f.write(generate_principles(principles))
            
            # Rights of the People
            rights = load_rights()
            f.write(generate_rights(rights))
            
            # Organizational overview
            f.write(generate_org_overview(conn))
            
            # District level
            f.write(generate_district_level(conn))
            
            # TODO: Add Regional and World levels (would continue similarly)
            # For now, this provides a substantial foundation
            
            # Glossary
            f.write(generate_glossary(conn))
        
        print(f"✓ Manuscript generated: {OUTPUT_PATH}")
        print(f"  Size: {OUTPUT_PATH.stat().st_size} bytes")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
