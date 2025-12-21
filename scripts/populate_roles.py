#!/usr/bin/env python3
"""
Populate roles and duties for all institutions.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'db' / 'terran_society.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_institution_id(conn, name, tier, branch):
    """Get institution ID by name, tier, and branch"""
    cur = conn.cursor()
    cur.execute('''
        SELECT InstitutionID FROM tInstitution 
        WHERE InstitutionName = ? AND TierName = ? AND BranchName = ?
    ''', (name, tier, branch))
    result = cur.fetchone()
    return result[0] if result else None

def populate_council_of_elders_roles(conn):
    """Council of Elders roles and duties"""
    inst_id = get_institution_id(conn, 'Council of Elders', 'District', 'Legislative')
    
    roles = [
        (inst_id, 'Elder', 'Elected Elder', 
         'Member of the District Council of Elders serving the community', 
         3, 0, None, None, 'Direct', 'council-of-elders:6', 1),
        (inst_id, 'Elder Council Chair', 'Council Chair', 
         'Coordinates Council meetings and agenda, elected by fellow Elders', 
         1, 0, None, None, 'Internal', 'Derived:CouncilChair', 2),
    ]
    
    cur = conn.cursor()
    for role_data in roles:
        cur.execute('''
            INSERT OR IGNORE INTO tRole 
            (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
             HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', role_data)
        
        role_id = cur.lastrowid
        if role_id:
            # Elder duties
            if 'Elder' in role_data[1] and 'Chair' not in role_data[1]:
                duties = [
                    ('Conflict Resolution', 'Peacefully resolve disputes between District members before escalation to Sheriff or Courts', 'council-of-elders:22', 1),
                    ('Family Support', 'Provide counsel and guidance to families in need, help restore family unity in crisis situations', 'council-of-elders:12-16', 2),
                    ('Child Welfare', 'Maintain safe haven for children in distress, oversee care of orphans and adoption process', 'council-of-elders:18', 3),
                    ('Community Assistance', 'Help people who are struggling to adapt to Terran Society or access benefits and services', 'council-of-elders:20', 4),
                    ('Youth Guidance', 'Address juvenile misbehavior through mentorship before involvement of authorities', 'Council_of_Elders_note:3', 5),
                    ('Community Liaison', 'Maintain good information flow to residents about District matters and Regional issues', 'Council_of_Elders_note:16', 6),
                    ('Social Cohesion', 'Facilitate simple social events that encourage neighbors to know one another', 'Council_of_Elders_note:18', 7),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))

def populate_regional_executive_roles(conn):
    """Regional Executive branch roles"""
    
    # Administrator
    inst_id = get_institution_id(conn, 'Office of Regional Administrator', 'Region', 'Executive')
    if inst_id:
        roles = [
            (inst_id, 'Regional Administrator', 'Regional Administrator', 
             'Chief administrative officer managing regional government operations and infrastructure', 
             3, 1, 9, 3, 'Direct', 'NewShape:418', 1),
            (inst_id, 'Deputy Administrator', 'Deputy Regional Administrator',
             'Assists Administrator and may act in their absence',
             3, 0, None, None, 'Appointed', 'Derived:DeputyAdmin', 2),
            (inst_id, 'Director of Elections', 'Director of Elections',
             'Manages clean, transparent election process including public forums for debate',
             3, 0, None, None, 'Appointed', 'NewShape:430', 3),
            (inst_id, 'Director of Infrastructure', 'Director of Infrastructure',
             'Oversees communications, networking, and infrastructure systems',
             3, 0, None, None, 'Appointed', 'NewShape:434', 4),
            (inst_id, 'Director of Public Services', 'Director of Public Services',
             'Coordinates creation and oversight of Public Service Cooperatives',
             3, 0, None, None, 'Appointed', 'NewShape:436', 5),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id and 'Regional Administrator' == role_data[1]:
                duties = [
                    ('Government Operations', 'Administer regional government buildings, facilities, operations and related staffing', 'NewShape:420', 1),
                    ('Election Administration', 'Ensure clean, well-managed election process with public forum for candidate debate', 'NewShape:430', 2),
                    ('Equitable Services', 'Ensure equitable distribution of benefits and services across all Districts', 'NewShape:432', 3),
                    ('Infrastructure Management', 'Oversee communications, networking, and infrastructure services and systems', 'NewShape:434', 4),
                    ('Public Service Cooperatives', 'Facilitate creation of Public Service Cooperatives for utilities, ports, transit, etc.', 'NewShape:436', 5),
                    ('Medical Facilities', 'Assure proper medical facilities and resources are available throughout the Region', 'NewShape:438', 6),
                    ('Fire Services', 'Maintain Fire Stations and conduct fire safety inspections and enforcement', 'NewShape:440', 7),
                    ('Cooperative Templates', 'Prepare organizational templates for cooperatives for legislative approval', 'NewShape:422', 8),
                    ('Cooperative Assistance', 'Assist people and organizations in applying for and launching approved cooperatives', 'NewShape:424', 9),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))
    
    # Treasurer
    inst_id = get_institution_id(conn, 'Office of Regional Treasurer', 'Region', 'Executive')
    if inst_id:
        roles = [
            (inst_id, 'Regional Treasurer', 'Regional Treasurer', 
             'Chief financial officer managing regional budget, taxation, and financial oversight', 
             3, 1, 9, 3, 'Direct', 'NewShape:443', 1),
            (inst_id, 'Deputy Treasurer', 'Deputy Regional Treasurer',
             'Assists Treasurer and manages specific financial departments',
             3, 0, None, None, 'Appointed', 'Derived:DeputyTreas', 2),
            (inst_id, 'Director of Budget', 'Budget Director',
             'Prepares budget proposals and monitors budget execution',
             3, 0, None, None, 'Appointed', 'NewShape:445', 3),
            (inst_id, 'Director of Audits', 'Audit Director',
             'Conducts audits of regional management, businesses, and cooperatives',
             3, 0, None, None, 'Appointed', 'NewShape:455', 4),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id and 'Regional Treasurer' == role_data[1]:
                duties = [
                    ('Budget Preparation', 'Prepare budget proposals for legislative approval on 1, 2, or 3 year cycles', 'NewShape:445', 1),
                    ('Benefits Accounts', 'Maintain a benefits account for each person residing in the Region', 'NewShape:447', 2),
                    ('Tax Administration', 'Administer taxation and collection as defined by legislation', 'NewShape:449', 3),
                    ('Regional Bank Oversight', 'Appoint five-member Board of Directors of Regional Bank, subject to legislative approval', 'NewShape:451', 4),
                    ('Cooperative Financial Support', 'Assist in conversion/creation of cooperatives from the financial perspective', 'NewShape:453', 5),
                    ('Audit Authority', 'Authority and duty to audit regional management, registered businesses, and cooperatives', 'NewShape:455', 6),
                    ('Forensic Investigation', 'Conduct forensic audit as part of criminal investigation when required', 'NewShape:457', 7),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))
    
    # Sheriff
    inst_id = get_institution_id(conn, 'Office of Regional Sheriff', 'Region', 'Executive')
    if inst_id:
        roles = [
            (inst_id, 'Regional Sheriff', 'Regional Sheriff', 
             'Chief law enforcement officer responsible for protecting Rights of the People', 
             3, 1, 9, 3, 'Direct', 'NewShape:471', 1),
            (inst_id, 'Deputy Sheriff', 'Deputy Regional Sheriff',
             'Senior law enforcement officer assisting Sheriff in operations',
             3, 0, None, None, 'Appointed', 'Derived:DepSheriff', 2),
            (inst_id, 'Marshal', 'Regional Marshal',
             'Field law enforcement officer trained in non-lethal force and investigation',
             3, 0, None, None, 'Appointed', 'NewShape:475', 3),
            (inst_id, 'Chief Investigator', 'Chief of Investigations',
             'Leads criminal investigations and forensic laboratory operations',
             3, 0, None, None, 'Appointed', 'NewShape:477', 4),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id and 'Regional Sheriff' == role_data[1]:
                duties = [
                    ('Rights Protection', 'Responsible for protecting the Rights of the People as primary duty', 'NewShape:473', 1),
                    ('Physical Fitness', 'Ensure officers are physically fit, trained in self-defense and safe non-lethal subduing techniques', 'NewShape:475', 2),
                    ('Criminal Investigation', 'Conduct criminal investigations and maintain forensic laboratory capabilities', 'NewShape:477', 3),
                    ('Emergency Response', 'Maintain accessibility and ability to respond to emergency calls of all types including rescue', 'NewShape:479-481', 4),
                    ('Inter-Regional Coordination', 'Coordinate with Planetary Sheriff on matters involving inter-regional crime', 'NewShape:483', 5),
                    ('Whistleblower Protection', 'Provide protection to members who report official misconduct or serious crime', 'NewShape:485', 6),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))
    
    # Ambassador
    inst_id = get_institution_id(conn, 'Office of Regional Ambassador', 'Region', 'Executive')
    if inst_id:
        roles = [
            (inst_id, 'Regional Ambassador', 'Regional Ambassador', 
             'Chief diplomatic officer promoting commerce, tourism, and regional interests', 
             3, 1, 9, 3, 'Direct', 'NewShape:460', 1),
            (inst_id, 'Deputy Ambassador', 'Deputy Regional Ambassador',
             'Assists Ambassador in diplomatic and economic development functions',
             3, 0, None, None, 'Appointed', 'Derived:DepAmbassador', 2),
            (inst_id, 'Economic Development Director', 'Director of Economic Development',
             'Promotes commerce, trade, and economic opportunities for the Region',
             3, 0, None, None, 'Appointed', 'NewShape:468', 3),
            (inst_id, 'Consular Officer', 'Regional Consular Officer',
             'Assists regional members traveling in other Regions',
             3, 0, None, None, 'Appointed', 'NewShape:464', 4),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id and 'Regional Ambassador' == role_data[1]:
                duties = [
                    ('Commerce Promotion', 'Promote commerce, tourism, and other economic development', 'NewShape:462', 1),
                    ('Traveler Assistance', 'Assist travelers in far away Regions and help residents vote when away from home', 'NewShape:464', 2),
                    ('Regional Image', 'Promote a positive and unifying image of the Region', 'NewShape:466', 3),
                    ('Inter-Regional Trade', 'Promote economic development and inter-regional trade opportunities', 'NewShape:468', 4),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))
    
    # Environmental Guardian
    inst_id = get_institution_id(conn, 'Office of Regional Environmental Guardian', 'Region', 'Executive')
    if inst_id:
        roles = [
            (inst_id, 'Regional Environmental Guardian', 'Regional Environmental Guardian', 
             'Chief environmental officer for regional environmental protection and restoration', 
             3, 1, 9, 3, 'Direct', 'NewShape:488', 1),
            (inst_id, 'Deputy Environmental Guardian', 'Deputy Regional Environmental Guardian',
             'Assists Environmental Guardian in environmental operations',
             3, 0, None, None, 'Appointed', 'Derived:DepEnvGuard', 2),
            (inst_id, 'Director of Environmental Monitoring', 'Environmental Monitoring Director',
             'Oversees pollution testing and environmental damage assessment',
             3, 0, None, None, 'Appointed', 'NewShape:492-494', 3),
            (inst_id, 'Director of Restoration', 'Ecosystem Restoration Director',
             'Plans and implements ecosystem restoration projects',
             3, 0, None, None, 'Appointed', 'NewShape:490', 4),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id and 'Regional Environmental Guardian' == role_data[1]:
                duties = [
                    ('Environmental Protection', 'Conduct regional environmental protection and ecosystem restoration operations', 'NewShape:490', 1),
                    ('Pollution Testing', 'Pro-actively test for pollution and environmental damage', 'NewShape:492', 2),
                    ('Data Consolidation', 'Consolidate environmental monitoring data and report to Planetary Environmental Guardian', 'NewShape:494', 3),
                    ('Methods Development', 'Develop and evaluate environmental protection techniques, methods, and technology', 'NewShape:496', 4),
                    ('Waste Management', 'Ensure toxic industrial byproducts are rendered stable before release to environment', 'NewShape:498', 5),
                    ('Resource Standards', 'Ensure natural resource extraction conforms to respectful, legislatively-determined standards', 'NewShape:501', 6),
                    ('Complaint Investigation', 'Receive and investigate environmental concern reports from members', 'NewShape:503', 7),
                    ('Remediation Planning', 'Determine plans for environmental repair and restoration, then implement them', 'NewShape:505', 8),
                    ('Resource Coordination', 'First point of dispute resolution and coordination regarding resources within Region', 'NewShape:507-509', 9),
                    ('Technical Assistance', 'Provide information and technical assistance to organizations with environmental impact', 'NewShape:511', 10),
                    ('Standards Proposal', 'Propose environmental and health safety standards to the Council of the People', 'NewShape:513', 11),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))

def populate_regional_legislative_roles(conn):
    """Regional Legislative branch roles"""
    inst_id = get_institution_id(conn, 'Regional Council of the People', 'Region', 'Legislative')
    if inst_id:
        roles = [
            (inst_id, 'Representative', 'Representative to Regional Council', 
             'Elected representative from a District to the Regional Council of the People', 
             3, 0, None, None, 'Direct', 'NewShape:350', 1),
            (inst_id, 'Council Speaker', 'Speaker of the Regional Council',
             'Presides over Council sessions, elected by Council members',
             1, 0, None, None, 'Internal', 'Derived:Speaker', 2),
            (inst_id, 'Council Clerk', 'Clerk of the Regional Council',
             'Maintains Council records, manages documentation and legislative process',
             3, 0, None, None, 'Appointed', 'Derived:Clerk', 3),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id and 'Representative' == role_data[1]:
                duties = [
                    ('Budget Approval', 'Approve regional budget on 1, 2, or 3 year cycle', 'NewShape:357', 1),
                    ('Cooperative Development', 'Work with Executive Council developing organizational models for Public Service Cooperatives', 'NewShape:359', 2),
                    ('Cooperative Chartering', 'Charter and fund approved public and private service cooperatives', 'NewShape:361', 3),
                    ('Investigative Hearings', 'Hold public investigative hearings as needed', 'NewShape:363', 4),
                    ('Environmental Standards', 'Legislate environmental protection standards for use of natural resources', 'NewShape:365', 5),
                    ('Resource Allocation', 'Allocate land and water resources fairly with objective standards', 'NewShape:367', 6),
                    ('Impeachment Authority', 'Impeach and remove elected officials of Executive, Judicial, or Fair Witness for cause', 'NewShape:369', 7),
                    ('Contributed Service Rules', 'Establish objective rules for Administrator to manage Contributed Service', 'NewShape:371', 8),
                    ('Veto Override', 'Override Executive Council veto with three-fourths majority vote', 'NewShape:373', 9),
                    ('Penalties Definition', 'Define major/minor violations and specify appropriate maximum and minimum penalties', 'NewShape:375', 10),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))

def populate_regional_judicial_roles(conn):
    """Regional Judicial branch roles"""
    
    # Facilitator of Court (Conductor)
    inst_id = get_institution_id(conn, 'Office of Facilitator of the Court', 'Region', 'Judicial')
    if inst_id:
        roles = [
            (inst_id, 'Facilitator of the Court', 'Facilitator of the Court (Conductor)', 
             'Presides over Major and Minor Courts, manages court process and advises jury', 
             6, 0, None, None, 'Direct', 'NewShape:629', 1),
            (inst_id, 'Court Administrator', 'Court System Administrator',
             'Manages court facilities, scheduling, jury coordination, and court staff',
             3, 0, None, None, 'Appointed', 'Derived:CourtAdmin', 2),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id and 'Facilitator of the Court' == role_data[1]:
                duties = [
                    ('Court Presiding', 'Preside over Minor and Major Court proceedings', 'NewShape:633', 1),
                    ('Case Classification', 'Determine in which type of court (Minor or Major) the case should be heard', 'NewShape:635', 2),
                    ('Jury Advising', 'Advise the jury, clarify issues, and answer their questions', 'NewShape:637', 3),
                    ('Case Dismissal', 'Dismiss a case if that is clearly the just course of action', 'NewShape:639', 4),
                    ('Mistrial Declaration', 'Abolish a Jury ruling or declare mistrial for cause and reschedule hearing', 'NewShape:641', 5),
                    ('Misconduct Management', 'Remove anyone, even a jury member, for misconduct', 'NewShape:643', 6),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))
    
    # Guarantor of Rights
    inst_id = get_institution_id(conn, 'Office of Guarantor of Rights', 'Region', 'Judicial')
    if inst_id:
        roles = [
            (inst_id, 'Guarantor of Rights', 'Guarantor of Rights', 
             'Investigates rights violations and serves as watchdog over Sheriff and Executive', 
             3, 1, 9, 3, 'Direct', 'NewShape:646', 1),
            (inst_id, 'Rights Investigator', 'Rights Investigator',
             'Investigates complaints of rights violations and gathers evidence',
             3, 0, None, None, 'Appointed', 'NewShape:648', 2),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id and 'Guarantor of Rights' == role_data[1]:
                duties = [
                    ('Rights Investigation', 'Investigate violations of Rights of the People', 'NewShape:648', 1),
                    ('Warrant Presentation', 'Present evidence to Warrant Jury when search, arrest, or court appearance is required', 'NewShape:648', 2),
                    ('Executive Oversight', 'Serve as watchdog of Sheriff and other Executive Branch officials for the People', 'NewShape:650', 3),
                    ('Impeachment Evidence', 'Present evidence for impeachment of officials to the legislative body', 'NewShape:652', 4),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))
    
    # Public Arbitrator
    inst_id = get_institution_id(conn, 'Office of Public Arbitrator', 'Region', 'Judicial')
    if inst_id:
        roles = [
            (inst_id, 'Public Arbitrator', 'Public Arbitrator', 
             'Provides voluntary arbitration services for dispute resolution', 
             3, 0, None, None, 'Direct', 'NewShape:655', 1),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id:
                duties = [
                    ('Case Selection', 'Choose to accept cases for arbitration hearings', 'NewShape:661', 1),
                    ('Arbitration Hearing', 'Conduct arbitration hearing and listen to all parties', 'NewShape:663', 2),
                    ('Ruling Determination', 'Determine a fair and just ruling after hearing the case', 'NewShape:663', 3),
                    ('Order Maintenance', 'Remove persons from hearing for misconduct', 'NewShape:665', 4),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))

def populate_fair_witness_roles(conn):
    """Fair Witness branch roles"""
    
    # Regional Fair Witness Council
    inst_id = get_institution_id(conn, 'Regional Fair Witness Council', 'Region', 'Fair Witness')
    if inst_id:
        roles = [
            (inst_id, 'Regional Fair Witness Councilor', 'Regional Fair Witness Councilor', 
             'Elected member of nine-person Regional Fair Witness Council', 
             9, 1, 18, 2, 'Internal', 'NewShape:764', 1),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
    
    # Fair Witness Training
    inst_id = get_institution_id(conn, 'Fair Witness Training Academy', 'Region', 'Fair Witness')
    if inst_id:
        roles = [
            (inst_id, 'Fair Witness Trainee', 'Fair Witness Trainee', 
             'Qualified person accepted into Fair Witness training program', 
             None, 0, None, None, None, 'NewShape:753', 1),
            (inst_id, 'Fair Witness Apprentice', 'Fair Witness Apprentice', 
             'Graduate of training program qualified to assist Certified Fair Witnesses', 
             None, 0, None, None, None, 'NewShape:755', 2),
            (inst_id, 'Certified Fair Witness', 'Certified Fair Witness (CFW)', 
             'Certified observer qualified to record proceedings and maintain public records', 
             None, 0, None, None, None, 'NewShape:757', 3),
            (inst_id, 'Senior Certified Fair Witness', 'Senior Certified Fair Witness (SCFW)', 
             'Senior Fair Witness with extensive honorable service', 
             None, 0, None, None, None, 'NewShape:759', 4),
            (inst_id, 'Training Director', 'Director of Fair Witness Training',
             'Oversees Fair Witness training academy and certification process',
             3, 0, None, None, 'Appointed', 'Derived:FWTraining', 5),
        ]
        
        cur = conn.cursor()
        for role_data in roles:
            cur.execute('''
                INSERT OR IGNORE INTO tRole 
                (InstitutionID, RoleName, RoleTitle, RoleDesc, TermLengthYears, 
                 HasTermLimit, TermLimitYears, MaxConsecutiveTerms, ElectionMethod, DocLoc, SortOrder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', role_data)
            
            role_id = cur.lastrowid
            if role_id and 'Certified Fair Witness' == role_data[1]:
                duties = [
                    ('Observation', 'Attend and observe meetings of Executive, Legislative, Judicial, and District Council', 'NewShape:726-735', 1),
                    ('Record Keeping', 'Create, publish, and maintain accurate records and libraries for public access', 'NewShape:724', 2),
                    ('Objective Documentation', 'Document events in clear, objective language without assumption or subjectivity', 'NewShape:740', 3),
                    ('Language Mastery', 'Maintain fluency in major languages and master linguistics and communication', 'NewShape:742-744', 4),
                    ('Evidence Provision', 'Provide accurate records that may serve as evidence, without conducting investigations', 'NewShape:746', 5),
                ]
                
                for header, desc, docloc, sort in duties:
                    cur.execute('''
                        INSERT OR IGNORE INTO tRoleDuty (RoleID, RoleDutyHeader, RoleDutyDesc, DocLoc, SortOrder)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (role_id, header, desc, docloc, sort))

def main():
    print("Populating roles and duties...")
    conn = get_connection()
    
    try:
        populate_council_of_elders_roles(conn)
        print("✓ Council of Elders roles")
        
        populate_regional_executive_roles(conn)
        print("✓ Regional Executive roles")
        
        populate_regional_legislative_roles(conn)
        print("✓ Regional Legislative roles")
        
        populate_regional_judicial_roles(conn)
        print("✓ Regional Judicial roles")
        
        populate_fair_witness_roles(conn)
        print("✓ Fair Witness roles")
        
        conn.commit()
        
        # Show summary
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tRole")
        print(f"\nRoles populated: {cur.fetchone()[0]} roles")
        cur.execute("SELECT COUNT(*) FROM tRoleDuty")
        print(f"                 {cur.fetchone()[0]} duties")
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
