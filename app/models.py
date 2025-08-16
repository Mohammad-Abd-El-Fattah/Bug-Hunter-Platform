import sqlite3
from datetime import datetime

DB_PATH = 'bug_hunter_enhanced.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS platforms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        url TEXT,
        platform_type TEXT, -- e.g., 'public', 'private', 'vdp'
        is_active INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS bug_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        severity TEXT,
        status TEXT,
        vulnerability_type TEXT,
        target_url TEXT,
        platform_id INTEGER,
        program_name TEXT,
        bounty_amount REAL DEFAULT 0,
        poc_steps TEXT,
        impact_description TEXT,
        remediation_suggestion TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS bounty_targets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        target_amount REAL,
        current_amount REAL DEFAULT 0,
        deadline DATE,
        is_active INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS security_checklists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        source_url TEXT, -- For GitHub import
        type TEXT,
        description TEXT,
        items TEXT,
        progress INTEGER DEFAULT 0,
        is_template INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS reading_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        is_read INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS news_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        url TEXT,
        source TEXT,
        category TEXT,
        published_at DATETIME
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS personal_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        category TEXT,
        tags TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS recon_campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_domain TEXT,
        status TEXT,
        script_name TEXT,
        log_path TEXT,
        is_stopped INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    # Add other tables as needed

    conn.commit()
    conn.close()

