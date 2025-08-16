-- Main tables
CREATE TABLE platforms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT,
    api_key TEXT,
    stats TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bug_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, description TEXT, severity TEXT, status TEXT,
    vulnerability_type TEXT, target_url TEXT,
    platform TEXT, program_name TEXT,
    bounty_amount REAL,
    poc_steps TEXT,
    impact_description TEXT,
    remediation_suggestion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bounty_targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, description TEXT,
    target_amount REAL, current_amount REAL,
    deadline DATE,
    is_active BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ... other tables as required

-- Additional tables for tips, notes, news, etc.
