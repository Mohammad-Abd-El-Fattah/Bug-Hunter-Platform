#!/usr/bin/env python3
"""
Bug Hunter Enhanced Dashboard - Complete Version
Fixed all routes and API endpoints
"""
import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from flask import Flask, render_template, request, jsonify, abort, redirect, url_for

# Optional feedparser (fallback for Python 3.13)
try:
    import feedparser
    FEED_OK = True
except Exception:
    FEED_OK = False

###############################################################################
# Configuration
###############################################################################
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "bug_hunter_enhanced.db"
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

###############################################################################
# Flask app
###############################################################################
app = Flask(__name__)
app.secret_key = "change-this-secret-key-in-production"

###############################################################################
# Database helpers
###############################################################################

def db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Create all required tables if they do not exist."""
    conn = db_connect()
    c = conn.cursor()

    # Platforms table
    c.execute("""
        CREATE TABLE IF NOT EXISTS platforms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT,
            platform_type TEXT DEFAULT 'public',
            api_key TEXT,
            is_active INTEGER DEFAULT 1,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Bug reports table
    c.execute("""
        CREATE TABLE IF NOT EXISTS bug_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            severity TEXT,
            status TEXT DEFAULT 'draft',
            vulnerability_type TEXT,
            target_url TEXT,
            platform TEXT,
            program_name TEXT,
            bounty_amount REAL DEFAULT 0,
            poc_steps TEXT,
            impact_description TEXT,
            remediation_suggestion TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Personal notes table
    c.execute("""
        CREATE TABLE IF NOT EXISTS personal_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            category TEXT DEFAULT 'general',
            tags TEXT,
            is_pinned INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Recon campaigns table
    c.execute("""
        CREATE TABLE IF NOT EXISTS recon_campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_domain TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            subdomain_count INTEGER DEFAULT 0,
            live_host_count INTEGER DEFAULT 0,
            scope_size TEXT DEFAULT 'medium',
            script_name TEXT,
            log_path TEXT,
            is_stopped INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Security checklists table
    c.execute("""
        CREATE TABLE IF NOT EXISTS security_checklists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT DEFAULT 'web',
            description TEXT,
            items TEXT,
            progress INTEGER DEFAULT 0,
            source_url TEXT,
            is_template INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tips and tricks table
    c.execute("""
        CREATE TABLE IF NOT EXISTS tips_tricks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            category TEXT DEFAULT 'general',
            difficulty TEXT DEFAULT 'beginner',
            tags TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Reading list table
    c.execute("""
        CREATE TABLE IF NOT EXISTS reading_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT,
            description TEXT,
            category TEXT DEFAULT 'article',
            is_read INTEGER DEFAULT 0,
            priority INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Useful links table
    c.execute("""
        CREATE TABLE IF NOT EXISTS useful_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT,
            category TEXT DEFAULT 'tools',
            tags TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # News articles table
    c.execute("""
        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            url TEXT,
            source TEXT,
            category TEXT,
            published_date DATETIME,
            is_read INTEGER DEFAULT 0,
            is_favorite INTEGER DEFAULT 0
        )
    """)

    # Attack scripts table
    c.execute("""
        CREATE TABLE IF NOT EXISTS attack_scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            filename TEXT,
            language TEXT DEFAULT 'bash',
            description TEXT,
            file_path TEXT,
            status TEXT DEFAULT 'ready',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Exploit scripts table
    c.execute("""
        CREATE TABLE IF NOT EXISTS exploit_scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            filename TEXT,
            language TEXT DEFAULT 'bash',
            description TEXT,
            file_path TEXT,
            status TEXT DEFAULT 'ready',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Bounty targets table
    c.execute("""
        CREATE TABLE IF NOT EXISTS bounty_targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            target_amount REAL,
            current_amount REAL DEFAULT 0,
            deadline DATE,
            is_active INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

###############################################################################
# Utility functions
###############################################################################

def safe_query_scalar(cursor: sqlite3.Cursor, query: str, args: tuple = ()) -> int:
    """Safely execute a scalar query and return integer result."""
    try:
        cursor.execute(query, args)
        result = cursor.fetchone()
        return int(result[0]) if result and result[0] is not None else 0
    except sqlite3.OperationalError as e:
        print(f"Database query error: {e}")
        return 0

def get_dashboard_stats() -> Dict[str, Any]:
    """Get dashboard statistics with error handling."""
    conn = db_connect()
    cursor = conn.cursor()
    
    stats = {
        "total_bugs": safe_query_scalar(cursor, "SELECT COUNT(*) FROM bug_reports"),
        "active_bugs": safe_query_scalar(cursor, "SELECT COUNT(*) FROM bug_reports WHERE status NOT IN ('resolved', 'bounty_awarded')"),
        "resolved_bugs": safe_query_scalar(cursor, "SELECT COUNT(*) FROM bug_reports WHERE status IN ('resolved', 'bounty_awarded')"),
        "total_bounties": float(safe_query_scalar(cursor, "SELECT COALESCE(SUM(bounty_amount), 0) FROM bug_reports")),
        "monthly_earnings": float(safe_query_scalar(cursor, "SELECT COALESCE(SUM(bounty_amount), 0) FROM bug_reports WHERE created_at >= date('now', 'start of month')")),
        "platforms_count": safe_query_scalar(cursor, "SELECT COUNT(*) FROM platforms WHERE is_active = 1"),
        "checklists_count": safe_query_scalar(cursor, "SELECT COUNT(*) FROM security_checklists"),
        "notes_count": safe_query_scalar(cursor, "SELECT COUNT(*) FROM personal_notes"),
        "active_targets": safe_query_scalar(cursor, "SELECT COUNT(*) FROM bounty_targets WHERE is_active = 1"),
        "total_targets": safe_query_scalar(cursor, "SELECT COUNT(*) FROM bounty_targets"),
        "total_campaigns": safe_query_scalar(cursor, "SELECT COUNT(*) FROM recon_campaigns"),
    }
    
    # Calculate success rate
    if stats["total_bugs"] > 0:
        stats["success_rate"] = round((stats["resolved_bugs"] / stats["total_bugs"]) * 100, 1)
    else:
        stats["success_rate"] = 0.0
    
    # Platform distribution
    try:
        cursor.execute("SELECT platform, COUNT(*) FROM bug_reports WHERE platform IS NOT NULL GROUP BY platform")
        stats["platform_distribution"] = dict(cursor.fetchall())
    except sqlite3.OperationalError:
        stats["platform_distribution"] = {}
    
    # Vulnerability distribution
    try:
        cursor.execute("SELECT vulnerability_type, COUNT(*) FROM bug_reports WHERE vulnerability_type IS NOT NULL GROUP BY vulnerability_type")
        stats["vuln_distribution"] = dict(cursor.fetchall())
    except sqlite3.OperationalError:
        stats["vuln_distribution"] = {}
    
    conn.close()
    return stats

def fetch_rss_news(limit: int = 30) -> List[Dict[str, Any]]:
    """Fetch news from RSS feeds with fallback."""
    if FEED_OK:
        try:
            feed = feedparser.parse("https://hackerone.com/hacktivity.rss")
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    "title": entry.get("title", "Untitled"),
                    "content": entry.get("summary", ""),
                    "url": entry.get("link", ""),
                    "source": "HackerOne Hacktivity",
                    "category": "hacktivity",
                    "published_date": entry.get("published", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                    "is_read": False,
                    "is_favorite": False
                })
            return articles
        except Exception as e:
            print(f"RSS parsing error: {e}")
    
    # Fallback mock data
    return [
        {
            "title": "Critical SQL Injection Found in Popular CMS",
            "content": "Security researchers discovered a critical SQL injection vulnerability affecting thousands of websites...",
            "url": "https://example.com/news/sql-injection",
            "source": "Security News",
            "category": "vulnerabilities",
            "published_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "is_read": False,
            "is_favorite": False
        },
        {
            "title": "New Bug Bounty Program Launches with $1M Pool",
            "content": "Tech giant announces comprehensive bug bounty program with record-breaking reward pool...",
            "url": "https://example.com/news/bounty-program",
            "source": "Bug Bounty News",
            "category": "programs",
            "published_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "is_read": False,
            "is_favorite": False
        },
        {
            "title": "XSS Vulnerability Discovered in Major Social Platform",
            "content": "Cross-site scripting vulnerability allows attackers to execute malicious code in user browsers...",
            "url": "https://example.com/news/xss-vulnerability",
            "source": "Vulnerability Research",
            "category": "research",
            "published_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "is_read": False,
            "is_favorite": False
        }
    ]

###############################################################################
# Main Routes
###############################################################################

@app.route("/")
def dashboard():
    """Dashboard page with statistics."""
    try:
        stats = get_dashboard_stats()
    except Exception as e:
        print(f"Dashboard error: {e}")
        stats = {
            "total_bugs": 0, "active_bugs": 0, "resolved_bugs": 0,
            "total_bounties": 0.0, "monthly_earnings": 0.0,
            "platforms_count": 0, "checklists_count": 0, "notes_count": 0,
            "active_targets": 0, "total_targets": 0, "total_campaigns": 0,
            "success_rate": 0.0, "platform_distribution": {}, "vuln_distribution": {}
        }
    
    return render_template("dashboard.html", stats=stats)

@app.route("/platforms")
def platforms():
    """Bug bounty platforms page."""
    conn = db_connect()
    platforms = conn.execute("SELECT * FROM platforms ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("platforms.html", platforms=[dict(p) for p in platforms])

@app.route("/bug_reports")
def bug_reports():
    """Bug reports page."""
    conn = db_connect()
    bugs = conn.execute("SELECT * FROM bug_reports ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("bug_reports.html", bugs=[dict(b) for b in bugs])

@app.route("/security_checklist")
def security_checklist():
    """Security checklist page."""
    conn = db_connect()
    checklists = conn.execute("SELECT * FROM security_checklists ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("checklist.html", checklists=[dict(c) for c in checklists])

@app.route("/tips_tricks")
def tips_tricks():
    """Tips and tricks page."""
    conn = db_connect()
    tips = conn.execute("SELECT * FROM tips_tricks ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("tips.html", tips=[dict(t) for t in tips])

@app.route("/reading_list")
def reading_list():
    """Reading list page."""
    conn = db_connect()
    reading = conn.execute("SELECT * FROM reading_list ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("reading.html", reading=[dict(r) for r in reading])

@app.route("/news_feed")
def news_feed():
    """Security news feed page."""
    articles = fetch_rss_news()
    return render_template("news.html", articles=articles)

@app.route("/personal_notes")
def personal_notes():
    """Personal notes page."""
    conn = db_connect()
    notes = conn.execute("SELECT * FROM personal_notes ORDER BY is_pinned DESC, created_at DESC").fetchall()
    conn.close()
    return render_template("notes.html", notes=[dict(n) for n in notes])

@app.route("/useful_links")
def useful_links():
    """Useful links page."""
    conn = db_connect()
    links = conn.execute("SELECT * FROM useful_links ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("links.html", links=[dict(l) for l in links])

@app.route("/recon")
def recon():
    """Reconnaissance page."""
    conn = db_connect()
    campaigns = conn.execute("SELECT * FROM recon_campaigns ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("recon.html", campaigns=[dict(c) for c in campaigns])

@app.route("/attack")
def attack():
    """Attack scripts page."""
    conn = db_connect()
    scripts = conn.execute("SELECT * FROM attack_scripts ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("attack.html", scripts=[dict(s) for s in scripts])

@app.route("/exploit")
def exploit():
    """Exploit scripts page."""
    conn = db_connect()
    scripts = conn.execute("SELECT * FROM exploit_scripts ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("exploit.html", scripts=[dict(s) for s in scripts])

###############################################################################
# API Endpoints - Dashboard Stats
###############################################################################

@app.route("/api/dashboard/stats")
def api_dashboard_stats():
    """API endpoint for dashboard statistics."""
    try:
        stats = get_dashboard_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

###############################################################################
# API Endpoints - Notes
###############################################################################

@app.route("/api/notes", methods=["GET", "POST"])
def api_notes():
    """Notes collection endpoint."""
    if request.method == "GET":
        conn = db_connect()
        notes = conn.execute("SELECT * FROM personal_notes ORDER BY is_pinned DESC, created_at DESC").fetchall()
        conn.close()
        data = []
        for note in notes:
            note_dict = dict(note)
            note_dict["tags"] = json.loads(note_dict["tags"] or "[]")
            note_dict["is_pinned"] = bool(note_dict["is_pinned"])
            data.append(note_dict)
        return jsonify({"data": data})
    
    # POST - Create new note
    data = request.get_json()
    conn = db_connect()
    conn.execute(
        "INSERT INTO personal_notes (title, content, category, tags, is_pinned) VALUES (?, ?, ?, ?, ?)",
        (data.get("title"), data.get("content"), data.get("category", "general"), 
         json.dumps(data.get("tags", [])), 1 if data.get("is_pinned") else 0)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route("/api/notes/<int:note_id>", methods=["GET", "PUT", "DELETE"])
def api_note(note_id):
    """Single note endpoint."""
    conn = db_connect()
    
    if request.method == "GET":
        note = conn.execute("SELECT * FROM personal_notes WHERE id = ?", (note_id,)).fetchone()
        conn.close()
        if not note:
            abort(404)
        note_dict = dict(note)
        note_dict["tags"] = json.loads(note_dict["tags"] or "[]")
        note_dict["is_pinned"] = bool(note_dict["is_pinned"])
        return jsonify({"data": note_dict})
    
    elif request.method == "PUT":
        data = request.get_json()
        conn.execute(
            "UPDATE personal_notes SET title=?, content=?, category=?, tags=?, is_pinned=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (data.get("title"), data.get("content"), data.get("category", "general"),
             json.dumps(data.get("tags", [])), 1 if data.get("is_pinned") else 0, note_id)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    
    elif request.method == "DELETE":
        conn.execute("DELETE FROM personal_notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

@app.route("/api/notes/<int:note_id>/toggle-pin", methods=["PATCH"])
def api_toggle_pin(note_id):
    """Toggle pin status of a note."""
    conn = db_connect()
    conn.execute("UPDATE personal_notes SET is_pinned = CASE WHEN is_pinned = 1 THEN 0 ELSE 1 END WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

###############################################################################
# API Endpoints - Bug Reports
###############################################################################

@app.route("/api/bugs", methods=["GET", "POST"])
def api_bugs():
    """Bug reports collection endpoint."""
    if request.method == "GET":
        conn = db_connect()
        bugs = conn.execute("SELECT * FROM bug_reports ORDER BY created_at DESC").fetchall()
        conn.close()
        return jsonify({"data": [dict(bug) for bug in bugs]})
    
    # POST - Create new bug report
    data = request.get_json()
    conn = db_connect()
    conn.execute("""
        INSERT INTO bug_reports (title, description, severity, status, vulnerability_type, target_url, 
                                platform, program_name, bounty_amount, poc_steps, impact_description, remediation_suggestion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("title"), data.get("description"), data.get("severity", "medium"),
        data.get("status", "draft"), data.get("vulnerability_type"), data.get("target_url"),
        data.get("platform"), data.get("program_name"), data.get("bounty_amount", 0),
        data.get("poc_steps"), data.get("impact_description"), data.get("remediation_suggestion")
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route("/api/bugs/<int:bug_id>", methods=["GET", "PUT", "DELETE"])
def api_bug(bug_id):
    """Single bug report endpoint."""
    conn = db_connect()
    
    if request.method == "GET":
        bug = conn.execute("SELECT * FROM bug_reports WHERE id = ?", (bug_id,)).fetchone()
        conn.close()
        if not bug:
            abort(404)
        return jsonify({"data": dict(bug)})
    
    elif request.method == "PUT":
        data = request.get_json()
        conn.execute("""
            UPDATE bug_reports SET title=?, description=?, severity=?, status=?, vulnerability_type=?, 
                                  target_url=?, platform=?, program_name=?, bounty_amount=?, poc_steps=?, 
                                  impact_description=?, remediation_suggestion=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (
            data.get("title"), data.get("description"), data.get("severity"), data.get("status"),
            data.get("vulnerability_type"), data.get("target_url"), data.get("platform"),
            data.get("program_name"), data.get("bounty_amount"), data.get("poc_steps"),
            data.get("impact_description"), data.get("remediation_suggestion"), bug_id
        ))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    
    elif request.method == "DELETE":
        conn.execute("DELETE FROM bug_reports WHERE id = ?", (bug_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

###############################################################################
# API Endpoints - Platforms
###############################################################################

@app.route("/api/platforms", methods=["GET", "POST"])
def api_platforms():
    """Platforms collection endpoint."""
    if request.method == "GET":
        conn = db_connect()
        platforms = conn.execute("SELECT * FROM platforms ORDER BY created_at DESC").fetchall()
        conn.close()
        return jsonify({"data": [dict(platform) for platform in platforms]})
    
    # POST - Create new platform
    data = request.get_json()
    conn = db_connect()
    conn.execute(
        "INSERT INTO platforms (name, url, platform_type, api_key, is_active, description) VALUES (?, ?, ?, ?, ?, ?)",
        (data.get("name"), data.get("url"), data.get("platform_type", "public"), 
         data.get("api_key"), 1 if data.get("is_active", True) else 0, data.get("description"))
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route("/api/platforms/<int:platform_id>", methods=["GET", "PUT", "DELETE"])
def api_platform(platform_id):
    """Single platform endpoint."""
    conn = db_connect()
    
    if request.method == "GET":
        platform = conn.execute("SELECT * FROM platforms WHERE id = ?", (platform_id,)).fetchone()
        conn.close()
        if not platform:
            abort(404)
        return jsonify({"data": dict(platform)})
    
    elif request.method == "PUT":
        data = request.get_json()
        conn.execute(
            "UPDATE platforms SET name=?, url=?, platform_type=?, api_key=?, is_active=?, description=? WHERE id=?",
            (data.get("name"), data.get("url"), data.get("platform_type"), data.get("api_key"),
             1 if data.get("is_active") else 0, data.get("description"), platform_id)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    
    elif request.method == "DELETE":
        conn.execute("DELETE FROM platforms WHERE id = ?", (platform_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

###############################################################################
# API Endpoints - Recon Campaigns
###############################################################################

@app.route("/api/recon/campaigns", methods=["GET"])
def api_recon_campaigns():
    """Get recon campaigns."""
    conn = db_connect()
    campaigns = conn.execute("SELECT * FROM recon_campaigns ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify({"data": [dict(campaign) for campaign in campaigns]})

@app.route("/api/recon/start", methods=["POST"])
def api_start_recon():
    """Start a new recon campaign."""
    data = request.get_json()
    conn = db_connect()
    conn.execute(
        "INSERT INTO recon_campaigns (target_domain, status, scope_size, script_name) VALUES (?, ?, ?, ?)",
        (data.get("target_domain"), "running", data.get("scope_size", "medium"), data.get("script_name", "default"))
    )
    conn.commit()
    campaign_id = conn.lastrowid
    conn.close()
    return jsonify({"status": "success", "campaign_id": campaign_id})

@app.route("/api/campaigns/<int:campaign_id>", methods=["GET", "DELETE"])
def api_campaign(campaign_id):
    """Single campaign endpoint."""
    conn = db_connect()
    
    if request.method == "GET":
        campaign = conn.execute("SELECT * FROM recon_campaigns WHERE id = ?", (campaign_id,)).fetchone()
        conn.close()
        if not campaign:
            abort(404)
        return jsonify({"data": dict(campaign)})
    
    elif request.method == "DELETE":
        conn.execute("DELETE FROM recon_campaigns WHERE id = ?", (campaign_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

@app.route("/api/campaigns/<int:campaign_id>/stop", methods=["PATCH"])
def api_stop_campaign(campaign_id):
    """Stop a running campaign."""
    conn = db_connect()
    conn.execute(
        "UPDATE recon_campaigns SET status='stopped', is_stopped=1, updated_at=CURRENT_TIMESTAMP WHERE id=?",
        (campaign_id,)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})
    
    
@app.route("/targets")
def targets():
    """Bounty/Testing targets page."""
    conn = db_connect()
    # استخدم جدول bounty_targets أو targets حسب مشروعك
    targets = conn.execute("SELECT * FROM bounty_targets ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("targets.html", targets=[dict(t) for t in targets])


###############################################################################
# API Endpoints - News
###############################################################################

@app.route("/api/news", methods=["GET"])
def api_news():
    """Get news articles."""
    articles = fetch_rss_news()
    return jsonify({"articles": articles})

@app.route("/api/news/refresh", methods=["POST"])
def api_refresh_news():
    """Refresh news feed."""
    articles = fetch_rss_news()
    return jsonify({"status": "success", "count": len(articles)})

###############################################################################
# Error Handlers
###############################################################################

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

###############################################################################
# Main
###############################################################################

if __name__ == "__main__":
    print("🚀 Bug Hunter Enhanced Dashboard starting...")
    print("📍 Initializing database...")
    init_db()
    print("📍 Access the dashboard at: http://127.0.0.1:5000")
    print("🔧 Debug mode enabled")
    app.run(host='127.0.0.1', port=5000, debug=True)
