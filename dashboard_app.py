#!/usr/bin/env python3
"""
Bug Hunter's Dashboard
A local web interface for reconnaissance campaign management
No authentication required - localhost only
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json
import subprocess
import threading
from datetime import datetime
import sqlite3
from pathlib import Path
import uuid

app = Flask(__name__)
app.secret_key = 'bug-hunter-local-dashboard-2025'

# Configuration
RESULTS_DIR = Path('results')
DATABASE_PATH = 'bug_hunter.db'

# Ensure directories exist
RESULTS_DIR.mkdir(exist_ok=True)

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Campaigns table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS campaigns (
        id TEXT PRIMARY KEY,
        target_domain TEXT NOT NULL,
        scope_size TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        subdomain_count INTEGER DEFAULT 0,
        live_host_count INTEGER DEFAULT 0,
        vulnerability_count INTEGER DEFAULT 0,
        output_directory TEXT
    )
    """)

    # Bug reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bug_reports (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        severity TEXT NOT NULL,
        description TEXT,
        target_url TEXT,
        poc TEXT,
        status TEXT DEFAULT 'open',
        platform TEXT,
        bounty_amount REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Targets table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS targets (
        id TEXT PRIMARY KEY,
        domain TEXT NOT NULL UNIQUE,
        program_name TEXT,
        platform TEXT,
        scope_type TEXT,
        in_scope BOOLEAN DEFAULT 1,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# Database helper functions
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def dashboard():
    """Main dashboard page"""
    conn = get_db_connection()

    # Get recent campaigns
    recent_campaigns = conn.execute(
        'SELECT * FROM campaigns ORDER BY created_at DESC LIMIT 5'
    ).fetchall()

    # Get statistics
    total_campaigns = conn.execute('SELECT COUNT(*) FROM campaigns').fetchone()[0]
    total_bugs = conn.execute('SELECT COUNT(*) FROM bug_reports').fetchone()[0]
    total_targets = conn.execute('SELECT COUNT(*) FROM targets').fetchone()[0]

    # Get active campaigns
    active_campaigns = conn.execute(
        'SELECT COUNT(*) FROM campaigns WHERE status = "running"'
    ).fetchone()[0]

    conn.close()

    return render_template('dashboard.html', 
                         recent_campaigns=recent_campaigns,
                         stats={
                             'total_campaigns': total_campaigns,
                             'total_bugs': total_bugs,
                             'total_targets': total_targets,
                             'active_campaigns': active_campaigns
                         })

@app.route('/recon')
def recon():
    """Recon page for running reconnaissance scripts"""
    conn = get_db_connection()
    campaigns = conn.execute(
        'SELECT * FROM campaigns ORDER BY created_at DESC'
    ).fetchall()
    conn.close()

    return render_template('recon.html', campaigns=campaigns)

@app.route('/api/recon/start', methods=['POST'])
def start_recon_api():
    """API endpoint to start reconnaissance"""
    data = request.get_json()
    target_domain = data.get('target_domain')
    scope_size = data.get('scope_size', 'auto')

    if not target_domain:
        return jsonify({'error': 'Target domain is required'}), 400

    # Create campaign
    campaign_id = str(uuid.uuid4())
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO campaigns (id, target_domain, scope_size, status) VALUES (?, ?, ?, ?)',
        (campaign_id, target_domain, scope_size, 'running')
    )
    conn.commit()
    conn.close()

    return jsonify({'status': 'started', 'campaign_id': campaign_id})

@app.route('/bugs')
def bug_reports():
    """Bug reports page"""
    conn = get_db_connection()
    bugs = conn.execute(
        'SELECT * FROM bug_reports ORDER BY created_at DESC'
    ).fetchall()
    conn.close()

    return render_template('bug_reports.html', bugs=bugs)

@app.route('/targets')
def targets():
    """Bounty targets page"""
    conn = get_db_connection()
    targets = conn.execute(
        'SELECT * FROM targets ORDER BY created_at DESC'
    ).fetchall()
    conn.close()

    return render_template('targets.html', targets=targets)

@app.route('/checklist')
def security_checklist():
    """Security checklist page"""
    return render_template('checklist.html')

@app.route('/tips')
def tips_tricks():
    """Tips and tricks page"""
    return render_template('tips.html')

@app.route('/reading')
def reading_list():
    """Reading list page"""
    return render_template('reading.html')

@app.route('/news')
def news_feed():
    """News feed page"""
    return render_template('news.html')

@app.route('/notes')
def personal_notes():
    """Personal notes page"""
    conn = get_db_connection()
    notes = conn.execute(
        'SELECT * FROM notes ORDER BY updated_at DESC'
    ).fetchall()
    conn.close()

    return render_template('notes.html', notes=notes)

@app.route('/links')
def useful_links():
    """Useful links page"""
    return render_template('links.html')

@app.route('/attack')
def attack():
    """Attack page"""
    return render_template('attack.html')

@app.route('/exploit')
def exploit():
    """Exploit page"""
    return render_template('exploit.html')

if __name__ == '__main__':
    init_db()
    print("🚀 Bug Hunter's Dashboard starting...")
    print("📍 Access the dashboard at: http://localhost:5000")
    print("🔧 No authentication required - localhost only")
    app.run(host='127.0.0.1', port=5000, debug=True)
