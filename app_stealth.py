"""
Xbox Game Pass Ultimate Stealth Web Interface
Version: 3.0.0 - Anti-Rate-Limit Edition
No proxies needed - Advanced stealth techniques
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_socketio import SocketIO, emit
import os
import json
import threading
import uuid
import zipfile
from datetime import datetime
import logging
from xbox_stealth import (
    start_stealth_checker, 
    generate_stealth_stats, 
    is_stealth_session_active, 
    stop_stealth_checker, 
    pause_stealth_checker,
    stealth_checkers
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xbox-stealth-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

# Stealth logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] XboxStealth: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('XboxStealth')

# Global variables
stealth_sessions = {}
stealth_threads = {}

@app.route('/')
def index():
    return redirect(url_for('stealth_dashboard'))

@app.route('/stealth')
def stealth_dashboard():
    return render_template('stealth_dashboard.html')

@app.route('/api/stealth/health')
def stealth_health_check():
    """Stealth health check"""
    return jsonify({
        'status': 'stealth_ready',
        'version': '3.0.0',
        'mode': 'ultra_stealth_anti_rate_limit',
        'timestamp': datetime.now().isoformat(),
        'active_sessions': len(stealth_sessions)
    })

@socketio.on('connect')
def handle_connect():
    session_id = str(uuid.uuid4())
    logger.info(f"🎮 Stealth client connected - Session: {session_id}")
    
    # Create stealth session directory
    session_dir = f"sessions/session_{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    
    # Initialize stealth session
    stealth_sessions[session_id] = {
        'connected_at': datetime.now(),
        'status': 'stealth_connected',
        'mode': 'ultra_stealth'
    }
    
    emit('stealth_session_initialized', {
        'session_id': session_id,
        'version': '3.0.0',
        'mode': 'ultra_stealth_anti_rate_limit',
        'features': ['smart_delays', 'human_behavior', 'anti_detection']
    })
    emit('stats_update', generate_stealth_stats(session_id))

@socketio.on('disconnect')
def handle_disconnect():
    logger.info("🔌 Stealth client disconnected")

@socketio.on('start_stealth_check')
def handle_start_stealth_check(data):
    """Start ultra-stealth checking"""
    logger.info(f"🎮 Ultra-stealth check request received")
    
    session_id = data.get('session_id')
    if not session_id or session_id not in stealth_sessions:
        emit('error', {'message': '❌ Invalid stealth session ID'})
        return

    combo_content = data.get('combo_content', '').strip()
    if not combo_content:
        emit('error', {'message': '❌ No account combinations provided'})
        return

    # Parse combos
    combos = []
    
    # Handle different line ending formats
    lines = combo_content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    
    for line in lines:
        line = line.strip()
        if line and ':' in line:
            try:
                # Split only on the first colon to handle passwords with colons
                parts = line.split(':', 1)
                if len(parts) == 2:
                    email, password = parts
                    email = email.strip()
                    password = password.strip()
                    
                    # Basic email validation
                    if '@' in email and len(password) > 0:
                        combos.append((email, password))
                        logger.debug(f"📧 Parsed account: {email}")
                    else:
                        logger.warning(f"⚠️ Invalid format: {line}")
            except ValueError as e:
                logger.warning(f"⚠️ Failed to parse line: {line} - {e}")
                continue

    if not combos:
        emit('error', {'message': '❌ No valid account combinations found. Use email:password format'})
        return

    logger.info(f"🎮 Successfully parsed {len(combos)} Xbox accounts")
    logger.info(f"🎮 Starting stealth validation for {len(combos)} Xbox accounts")

    # Start stealth checker in background thread
    if session_id not in stealth_threads or not stealth_threads[session_id].is_alive():
        stealth_thread = threading.Thread(
            target=start_stealth_checker,
            args=(combos, session_id, socketio),
            daemon=True
        )
        stealth_threads[session_id] = stealth_thread
        stealth_thread.start()
        
        emit('stealth_check_started', {
            'total_accounts': len(combos),
            'mode': 'ultra_stealth',
            'estimated_time': f"{len(combos) * 8} seconds"
        })
    else:
        emit('error', {'message': '⚠️ Stealth checker already running for this session'})

@socketio.on('pause_stealth_check')
def handle_pause_stealth_check(data):
    """Pause stealth checking"""
    session_id = data.get('session_id')
    if session_id in stealth_sessions:
        pause_stealth_checker(session_id)
        emit('stealth_check_paused', {'session_id': session_id})
        logger.info(f"⏸️ Stealth checker paused for session {session_id}")

@socketio.on('stop_stealth_check')
def handle_stop_stealth_check(data):
    """Stop stealth checking"""
    session_id = data.get('session_id')
    if session_id in stealth_sessions:
        stop_stealth_checker(session_id)
        emit('stealth_check_stopped', {'session_id': session_id})
        logger.info(f"⏹️ Stealth checker stopped for session {session_id}")

@socketio.on('get_stealth_stats')
def handle_get_stealth_stats(data):
    """Get current stealth statistics"""
    session_id = data.get('session_id')
    if session_id:
        stats = generate_stealth_stats(session_id)
        emit('stats_update', stats)

@app.route('/api/stealth/download/<session_id>/<file_type>')
def download_stealth_results(session_id, file_type):
    """Download stealth results"""
    session_dir = f"sessions/session_{session_id}"
    
    file_mapping = {
        'ultimate': 'stealth_ultimate_hits.txt',
        'core': 'stealth_core_accounts.txt', 
        'pc_console': 'stealth_pc_console_accounts.txt',
        'free': 'stealth_free_accounts.txt',
        'invalid': 'stealth_invalid_accounts.txt',
        'errors': 'stealth_errors.txt',
        'all': 'all_results.zip'
    }
    
    if file_type == 'all':
        # Create ZIP with all results
        zip_path = f"{session_dir}/all_results.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for result_file in file_mapping.values():
                if result_file != 'all_results.zip':
                    file_path = f"{session_dir}/{result_file}"
                    if os.path.exists(file_path):
                        zipf.write(file_path, result_file)
        
        if os.path.exists(zip_path):
            return send_file(zip_path, as_attachment=True, download_name=f"xbox_stealth_results_{session_id}.zip")
    else:
        filename = file_mapping.get(file_type)
        if filename:
            file_path = f"{session_dir}/{filename}"
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True, download_name=filename)
    
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/stealth/sessions')
def list_stealth_sessions():
    """List all stealth sessions"""
    sessions = []
    if os.path.exists('sessions'):
        for session_folder in os.listdir('sessions'):
            if session_folder.startswith('session_'):
                session_id = session_folder.replace('session_', '')
                session_path = f"sessions/{session_folder}"
                
                # Get session stats
                stats = generate_stealth_stats(session_id)
                stats['session_id'] = session_id
                stats['created_at'] = datetime.fromtimestamp(
                    os.path.getctime(session_path)
                ).isoformat() if os.path.exists(session_path) else None
                
                sessions.append(stats)
    
    return jsonify({'sessions': sessions})

@app.route('/api/debug/parse-combos', methods=['POST'])
def debug_parse_combos():
    """Debug endpoint to test combo parsing"""
    try:
        data = request.get_json()
        combo_content = data.get('combo_content', '')
        
        # Parse combos using the same logic
        combos = []
        lines = combo_content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        
        debug_info = {
            'raw_content': combo_content,
            'raw_length': len(combo_content),
            'lines_count': len(lines),
            'lines': [],
            'parsed_combos': [],
            'errors': []
        }
        
        for i, line in enumerate(lines):
            line_info = {
                'line_number': i + 1,
                'raw_line': repr(line),
                'stripped_line': line.strip(),
                'has_colon': ':' in line,
                'parsed': False
            }
            
            line = line.strip()
            if line and ':' in line:
                try:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        email, password = parts
                        email = email.strip()
                        password = password.strip()
                        
                        if '@' in email and len(password) > 0:
                            combos.append((email, password))
                            debug_info['parsed_combos'].append({
                                'line': i + 1,
                                'email': email,
                                'password': '*' * len(password)  # Hide password
                            })
                            line_info['parsed'] = True
                        else:
                            debug_info['errors'].append(f"Line {i + 1}: Invalid email or empty password")
                except Exception as e:
                    debug_info['errors'].append(f"Line {i + 1}: {str(e)}")
            
            debug_info['lines'].append(line_info)
        
        debug_info['total_parsed'] = len(combos)
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def create_directories():
    """Create necessary directories"""
    os.makedirs('sessions', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

if __name__ == '__main__':
    create_directories()
    logger.info("🎮 Xbox Game Pass Ultimate Stealth Validator v3.0.0 starting...")
    logger.info("🥷 Ultra-stealth mode activated - No proxies needed!")
    
    # Use port from environment variable for Fly.io deployment, default to 5000
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
