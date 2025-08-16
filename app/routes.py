from flask import Blueprint, request, jsonify, render_template
from .models import *
import sqlite3
from datetime import datetime
import feedparser

bp = Blueprint('main', __name__)

# Utility function for DB connection
def get_db():
    return sqlite3.connect(DB_PATH)

# Dashboard
@bp.route('/')
def dashboard():
    try:
        stats = get_dashboard_stats()
        # Handle cases where key might be missing or tuple
        for key in ['active_bugs', 'resolved_bugs', 'active_targets', 'total_targets', 'total_bounties', 'monthly_earnings']:
            if isinstance(stats.get(key), tuple):
                stats[key] = stats[key][0]
            elif stats.get(key) is None:
                stats[key] = 0
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        print(f'Dashboard error: {e}')
        # Return default safe values
        return render_template('dashboard.html', stats={
            'total_bugs': 0, 'active_bugs': 0, 'resolved_bugs': 0, 'total_bounties': 0,
            'monthly_earnings': 0, 'platforms_count': 0, 'active_targets':0, 'total_targets':0,
            'total_campaigns':0, 'success_rate':0
        })

# Example: Platforms management
@bp.route('/api/platforms', methods=['GET', 'POST'])
def manage_platforms():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'GET':
        c.execute('SELECT * FROM platforms WHERE is_active=1')
        platforms = c.fetchall()
        return jsonify(platforms)
    elif request.method == 'POST':
        data = request.json
        c.execute('INSERT INTO platforms (name, url, platform_type) VALUES (?, ?, ?)',
                  (data['name'], data['url'], data['platform_type']))
        conn.commit()
        conn.close()
        return jsonify({'status':'ok'})

@bp.route('/api/platforms/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_platform(id):
    conn = get_db()
    c = conn.cursor()
    if request.method == 'PUT':
        data = request.json
        c.execute('UPDATE platforms SET name=?, url=?, platform_type=? WHERE id=?',
                  (data['name'], data['url'], data['platform_type'], id))
        conn.commit()
        conn.close()
        return jsonify({'status':'updated'})
    elif request.method == 'DELETE':
        c.execute('UPDATE platforms SET is_active=0 WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'status':'deleted'})

# CRUD for bug reports with update/delete
@bp.route('/api/bugs/<int:id>', methods=['PUT', 'DELETE'])
def bug_report_modify(id):
    conn = get_db()
    c = conn.cursor()
    if request.method == 'PUT':
        data = request.json
        c.execute('''UPDATE bug_reports SET title=?, description=?, severity=?, status=?, 
                     vulnerability_type=?, target_url=?, platform_id=?, program_name=?, 
                     bounty_amount=?, poc_steps=?, impact_description=?, remediation_suggestion=?, 
                     updated_at=? WHERE id=?''',
                  (data['title'], data['description'], data['severity'], data['status'], data['vulnerability_type'],
                   data['target_url'], data['platform_id'], data['program_name'], data['bounty_amount'],
                   data['poc_steps'], data['impact_description'], data['remediation_suggestion'], datetime.now(), id))
        conn.commit()
        conn.close()
        return jsonify({'status':'updated'})
    elif request.method == 'DELETE':
        c.execute('DELETE FROM bug_reports WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'status':'deleted'})

# Import security checklists from GitHub or add manual
@bp.route('/api/checklists/import', methods=['POST'])
def import_checklist():
    url = request.json.get('url')
    # Fetch and parse checklist from URL (e.g., GitHub)
    # Save in database's source_url
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO security_checklists (name, source_url, type) VALUES (?, ?, ?)', ('Imported Checklist', url, 'web'))
    conn.commit()
    conn.close()
    return jsonify({'status':'imported'})

# Tips CRUD
@bp.route('/api/tips', methods=['POST', 'PUT', 'DELETE'])
def tips_crud():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        data = request.json
        c.execute('INSERT INTO tips (title, content) VALUES (?, ?)', (data['title'], data['content']))
    elif request.method == 'PUT':
        data = request.json
        c.execute('UPDATE tips SET title=?, content=? WHERE id=?', (data['title'], data['content'], data['id']))
    elif request.method == 'DELETE':
        tip_id = request.args.get('id')
        c.execute('DELETE FROM tips WHERE id=?', (tip_id,))
    conn.commit()
    conn.close()
    return jsonify({'status':'ok'})

# Reading list CRUD
@bp.route('/api/reading_list', methods=['POST', 'PUT', 'DELETE'])
def reading_list_crud():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        data = request.json
        c.execute('INSERT INTO reading_list (title, url) VALUES (?, ?)', (data['title'], data['url']))
    elif request.method == 'PUT':
        data = request.json
        c.execute('UPDATE reading_list SET title=?, url=?, is_read=? WHERE id=?', 
                  (data['title'], data['url'], data.get('is_read', 0), data['id']))
    elif request.method == 'DELETE':
        note_id = request.args.get('id')
        c.execute('DELETE FROM reading_list WHERE id=?', (note_id,))
    conn.commit()
    conn.close()
    return jsonify({'status':'ok'})

# News RSS fetching
@bp.route('/api/news/update')
def update_news():
    # Fetch latest Hacktivity and HackerOne feeds, insert into news_articles
    # Use feedparser here
    feed = feedparser.parse('https://hackerone.com/hacktivity.rss')
    conn = get_db()
    c = conn.cursor()
    for entry in feed.entries[:50]:
        c.execute('''
            INSERT OR IGNORE INTO news_articles (title, url, source, category, published_at)
            VALUES (?, ?, 'HackerOne', 'hacktivity', ?)''',
            (entry.title, entry.link, entry.published))
    conn.commit()
    conn.close()
    return jsonify({'status':'updated'})

# Personal Notes CRUD
@bp.route('/api/notes', methods=['POST', 'PUT', 'DELETE'])
def notes_crud():
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        data = request.json
        c.execute('INSERT INTO personal_notes (title, content, category, tags) VALUES (?, ?, ?, ?)',
                  (data['title'], data['content'], data['category'], data.get('tags')))
    elif request.method == 'PUT':
        data = request.json
        c.execute('UPDATE personal_notes SET title=?, content=?, category=?, tags=? WHERE id=?',
                  (data['title'], data['content'], data['category'], data['tags'], data['id']))
    elif request.method == 'DELETE':
        note_id = request.args.get('id')
        c.execute('DELETE FROM personal_notes WHERE id=?', (note_id,))
    conn.commit()
    conn.close()
    return jsonify({'status':'ok'})

# Reconciliation and attack management
@bp.route('/api/recon/start', methods=['POST'])
def start_recon():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO recon_campaigns (target_domain, status, script_name) VALUES (?, ?, ?)',
              (data['target_domain'], 'running', data.get('script_name', 'default')))
    conn.commit()
    conn.close()
    return jsonify({'status':'started'})

@bp.route('/api/campaigns/<int:id>', methods=['DELETE', 'PATCH'])
def manage_campaign(id):
    conn = get_db()
    c = conn.cursor()
    if request.method == 'DELETE':
        c.execute('DELETE FROM recon_campaigns WHERE id=?', (id,))
    elif request.method == 'PATCH':
        # stop/start
        c.execute('UPDATE recon_campaigns SET is_stopped=1 WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status':'updated'})

# Attack / Exploit upload & management
@bp.route('/api/attack/upload', methods=['POST'])
def upload_attack_script():
    file = request.files['script']
    # Save file, create record
    filename = f"attack_scripts/{file.filename}"
    file.save(filename)
    return jsonify({'status':'uploaded', 'file_path': filename})

@bp.route('/api/attack/<int:id>/stop', methods=['PATCH'])
def stop_attack(id):
    # Logic to stop attack (update database record)
    return jsonify({'status':'stopped'})

@bp.route('/api/attack/<int:id>', methods=['DELETE'])
def delete_attack(id):
    # Remove attack script
    return jsonify({'status':'deleted'})

# Similar for exploit
@bp.route('/api/exploit/upload', methods=['POST'])
def upload_exploit_script():
    file = request.files['script']
    filename = f"exploit_scripts/{file.filename}"
    file.save(filename)
    return jsonify({'status':'uploaded', 'file_path': filename})

@bp.route('/api/exploit/<int:id>/stop', methods=['PATCH'])
def stop_exploit(id):
    return jsonify({'status':'stopped'})

@bp.route('/api/exploit/<int:id>', methods=['DELETE'])
def delete_exploit(id):
    return jsonify({'status':'deleted'})

# Register Blueprint
def init_routes(app):
    app.register_blueprint(bp)

