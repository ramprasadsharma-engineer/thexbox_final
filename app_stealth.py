"""
Xbox Game Pass Ultimate Stealth Web Interface
Version: 3.1.0 - Enhanced Security & Performance Edition
No proxies needed - Advanced stealth techniques with enhanced features
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit, disconnect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import json
import threading
import uuid
import zipfile
from datetime import datetime, timedelta
import logging
import hashlib
import secrets
from functools import wraps
import time
from xbox_stealth import (
    start_stealth_checker, 
    generate_stealth_stats, 
    is_stealth_session_active, 
    stop_stealth_checker, 
    pause_stealth_checker,
    stealth_checkers
)

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Enhanced security
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Enhanced rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False, 
                   ping_timeout=60, ping_interval=25)

# Enhanced logging with rotation
import logging.handlers
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = logging.handlers.RotatingFileHandler(
    'logs/xbox_stealth.log', 
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)

console_handler = logging.StreamHandler()

formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger = logging.getLogger('XboxStealth')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Global variables with enhanced session management
stealth_sessions = {}
stealth_threads = {}
session_activity = {}
max_sessions_per_ip = 3
session_timeout = 3600  # 1 hour

# Security middleware
def require_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'session_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def cleanup_expired_sessions():
    """Clean up expired sessions"""
    current_time = time.time()
    expired_sessions = []
    
    for session_id, data in stealth_sessions.items():
        if current_time - data.get('last_activity', 0) > session_timeout:
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        if session_id in stealth_threads:
            stop_stealth_checker(session_id)
            del stealth_threads[session_id]
        del stealth_sessions[session_id]
        logger.info(f"🧹 Cleaned up expired session: {session_id}")

# Cleanup thread
def cleanup_thread():
    while True:
        time.sleep(300)  # Run every 5 minutes
        cleanup_expired_sessions()

cleanup_thread_instance = threading.Thread(target=cleanup_thread, daemon=True)
cleanup_thread_instance.start()

@app.route('/')
def index():
    return redirect(url_for('stealth_dashboard'))

@app.route('/stealth')
def stealth_dashboard():
    return render_template('stealth_dashboard.html')

@app.route('/api/stealth/health')
@limiter.limit("10 per minute")
def stealth_health_check():
    """Enhanced stealth health check with performance metrics"""
    try:
        # Get system metrics
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return jsonify({
            'status': 'stealth_ready',
            'version': '3.1.0',
            'mode': 'enhanced_stealth_anti_rate_limit',
            'timestamp': datetime.now().isoformat(),
            'active_sessions': len(stealth_sessions),
            'system_metrics': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent
            },
            'uptime': time.time() - app.start_time if hasattr(app, 'start_time') else 0
        })
    except ImportError:
        return jsonify({
            'status': 'stealth_ready',
            'version': '3.1.0',
            'mode': 'enhanced_stealth_anti_rate_limit',
            'timestamp': datetime.now().isoformat(),
            'active_sessions': len(stealth_sessions),
            'note': 'psutil not available for system metrics'
        })

@app.route('/api/stealth/sessions')
@limiter.limit("20 per minute")
def get_active_sessions():
    """Get active sessions with enhanced information"""
    try:
        sessions_info = []
        for session_id, data in stealth_sessions.items():
            session_info = {
                'session_id': session_id,
                'status': data.get('status', 'unknown'),
                'connected_at': data.get('connected_at', '').isoformat() if isinstance(data.get('connected_at'), datetime) else str(data.get('connected_at')),
                'last_activity': data.get('last_activity', 0),
                'mode': data.get('mode', 'ultra_stealth'),
                'is_active': session_id in stealth_threads and stealth_threads[session_id].is_alive()
            }
            sessions_info.append(session_info)
        
        return jsonify({
            'sessions': sessions_info,
            'total_sessions': len(sessions_info),
            'max_sessions': max_sessions_per_ip
        })
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        return jsonify({'error': 'Failed to get sessions'}), 500

@socketio.on('connect')
def handle_connect():
    """Enhanced connection handling with session limits"""
    try:
        # Check IP-based session limits
        client_ip = request.remote_addr
        ip_sessions = sum(1 for s in stealth_sessions.values() if s.get('client_ip') == client_ip)
        
        if ip_sessions >= max_sessions_per_ip:
            emit('error', {'message': f'❌ Maximum sessions ({max_sessions_per_ip}) reached for your IP address'})
            disconnect()
            return
        
        session_id = str(uuid.uuid4())
        logger.info(f"🎮 Enhanced stealth client connected - Session: {session_id} from IP: {client_ip}")
        
        # Create enhanced session directory
        session_dir = f"sessions/session_{session_id}"
        os.makedirs(session_dir, exist_ok=True)
        
        # Initialize enhanced stealth session
        stealth_sessions[session_id] = {
            'connected_at': datetime.now(),
            'last_activity': time.time(),
            'status': 'stealth_connected',
            'mode': 'enhanced_stealth',
            'client_ip': client_ip,
            'session_dir': session_dir,
            'features': ['smart_delays', 'human_behavior', 'anti_detection', 'enhanced_security']
        }
        
        emit('stealth_session_initialized', {
            'session_id': session_id,
            'version': '3.1.0',
            'mode': 'enhanced_stealth_anti_rate_limit',
            'features': ['smart_delays', 'human_behavior', 'anti_detection', 'enhanced_security'],
            'session_limits': {
                'max_sessions_per_ip': max_sessions_per_ip,
                'session_timeout': session_timeout
            }
        })
        emit('stats_update', generate_stealth_stats(session_id))
        
    except Exception as e:
        logger.error(f"Error in connection handling: {e}")
        emit('error', {'message': '❌ Connection error occurred'})

@socketio.on('disconnect')
def handle_disconnect():
    """Enhanced disconnect handling"""
    try:
        logger.info("🔌 Enhanced stealth client disconnected")
        # Cleanup will be handled by the cleanup thread
    except Exception as e:
        logger.error(f"Error in disconnect handling: {e}")

@socketio.on('start_stealth_check')
@limiter.limit("5 per minute")
def handle_start_stealth_check(data):
    """Enhanced ultra-stealth checking with validation"""
    try:
        logger.info(f"🎮 Enhanced ultra-stealth check request received")
        
        session_id = data.get('session_id')
        if not session_id or session_id not in stealth_sessions:
            emit('error', {'message': '❌ Invalid stealth session ID'})
            return

        # Update session activity
        stealth_sessions[session_id]['last_activity'] = time.time()
        
        combo_content = data.get('combo_content', '').strip()
        if not combo_content:
            emit('error', {'message': '❌ No account combinations provided'})
            return

        # Enhanced combo parsing with validation
        combos = []
        invalid_lines = []
        
        # Handle different line ending formats
        lines = combo_content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line and ':' in line:
                try:
                    # Split only on the first colon to handle passwords with colons
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        email, password = parts
                        email = email.strip()
                        password = password.strip()
                        
                        # Enhanced email validation
                        if '@' in email and len(password) > 0 and len(email) <= 254:
                            combos.append((email, password))
                            logger.debug(f"📧 Parsed account: {email}")
                        else:
                            invalid_lines.append(f"Line {line_num}: Invalid email format or password")
                    else:
                        invalid_lines.append(f"Line {line_num}: Missing colon separator")
                except ValueError as e:
                    invalid_lines.append(f"Line {line_num}: Parsing error - {e}")
                    continue

        if not combos:
            emit('error', {'message': '❌ No valid account combinations found. Use email:password format'})
            return

        # Log validation results
        logger.info(f"🎮 Successfully parsed {len(combos)} Xbox accounts")
        if invalid_lines:
            logger.warning(f"⚠️ {len(invalid_lines)} invalid lines found")
            emit('warning', {'message': f'⚠️ {len(invalid_lines)} invalid lines found', 'details': invalid_lines})

        # Enhanced thread management
        if session_id not in stealth_threads or not stealth_threads[session_id].is_alive():
            stealth_thread = threading.Thread(
                target=start_stealth_checker,
                args=(combos, session_id, socketio),
                daemon=True,
                name=f"StealthChecker-{session_id}"
            )
            stealth_threads[session_id] = stealth_thread
            stealth_thread.start()
            
            # Enhanced time estimation
            estimated_time = len(combos) * 8  # 8 seconds per account
            hours = estimated_time // 3600
            minutes = (estimated_time % 3600) // 60
            seconds = estimated_time % 60
            
            time_str = ""
            if hours > 0:
                time_str += f"{hours}h "
            if minutes > 0:
                time_str += f"{minutes}m "
            time_str += f"{seconds}s"
            
            emit('stealth_check_started', {
                'total_accounts': len(combos),
                'mode': 'enhanced_stealth',
                'estimated_time': time_str,
                'invalid_lines_count': len(invalid_lines)
            })
        else:
            emit('error', {'message': '⚠️ Stealth checker already running for this session'})
            
    except Exception as e:
        logger.error(f"Error in start stealth check: {e}")
        emit('error', {'message': f'❌ Error starting stealth check: {str(e)}'})

@socketio.on('pause_stealth_check')
def handle_pause_stealth_check(data):
    """Enhanced pause stealth checking with session validation"""
    try:
        session_id = data.get('session_id')
        if session_id in stealth_sessions:
            # Update session activity
            stealth_sessions[session_id]['last_activity'] = time.time()
            
            pause_stealth_checker(session_id)
            emit('stealth_check_paused', {'session_id': session_id})
            logger.info(f"⏸️ Enhanced stealth checker paused for session {session_id}")
        else:
            emit('error', {'message': '❌ Invalid session ID for pause operation'})
    except Exception as e:
        logger.error(f"Error pausing stealth check: {e}")
        emit('error', {'message': f'❌ Error pausing stealth check: {str(e)}'})

@socketio.on('stop_stealth_check')
def handle_stop_stealth_check(data):
    """Enhanced stop stealth checking with cleanup"""
    try:
        session_id = data.get('session_id')
        if session_id in stealth_sessions:
            # Update session activity
            stealth_sessions[session_id]['last_activity'] = time.time()
            
            stop_stealth_checker(session_id)
            emit('stealth_check_stopped', {'session_id': session_id})
            logger.info(f"⏹️ Enhanced stealth checker stopped for session {session_id}")
            
            # Clean up thread reference
            if session_id in stealth_threads:
                del stealth_threads[session_id]
        else:
            emit('error', {'message': '❌ Invalid session ID for stop operation'})
    except Exception as e:
        logger.error(f"Error stopping stealth check: {e}")
        emit('error', {'message': f'❌ Error stopping stealth check: {str(e)}'})

@socketio.on('get_stealth_stats')
def handle_get_stealth_stats(data):
    """Enhanced stealth statistics with session validation"""
    try:
        session_id = data.get('session_id')
        if session_id and session_id in stealth_sessions:
            # Update session activity
            stealth_sessions[session_id]['last_activity'] = time.time()
            
            stats = generate_stealth_stats(session_id)
            emit('stats_update', stats)
        else:
            emit('error', {'message': '❌ Invalid session ID for stats request'})
    except Exception as e:
        logger.error(f"Error getting stealth stats: {e}")
        emit('error', {'message': f'❌ Error getting stats: {str(e)}'})

@app.route('/api/stealth/download/<session_id>/<file_type>')
@limiter.limit("30 per hour")
def download_stealth_results(session_id, file_type):
    """Enhanced download with session validation and security"""
    try:
        # Validate session exists
        if session_id not in stealth_sessions:
            return jsonify({'error': 'Invalid session ID'}), 404
            
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
            # Create enhanced ZIP with all results
            zip_path = f"{session_dir}/all_results.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for result_file in file_mapping.values():
                    if result_file != 'all_results.zip':
                        file_path = f"{session_dir}/{result_file}"
                        if os.path.exists(file_path):
                            zipf.write(file_path, result_file)
            
            if os.path.exists(zip_path):
                return send_file(
                    zip_path, 
                    as_attachment=True, 
                    download_name=f"xbox_stealth_results_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                )
        else:
            filename = file_mapping.get(file_type)
            if filename:
                file_path = f"{session_dir}/{filename}"
                if os.path.exists(file_path):
                    return send_file(
                        file_path, 
                        as_attachment=True, 
                        download_name=f"{file_type}_{filename}"
                    )
        
        return jsonify({'error': 'File not found'}), 404
        
    except Exception as e:
        logger.error(f"Error downloading results: {e}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/api/stealth/export/<session_id>')
@limiter.limit("20 per hour")
def export_session_data(session_id):
    """Export comprehensive session data"""
    try:
        if session_id not in stealth_sessions:
            return jsonify({'error': 'Invalid session ID'}), 404
            
        session_data = stealth_sessions[session_id]
        session_dir = f"sessions/session_{session_id}"
        
        # Get all result files
        result_files = {}
        for file_type in ['ultimate', 'core', 'pc_console', 'free', 'invalid', 'errors']:
            file_path = f"{session_dir}/stealth_{file_type}_accounts.txt"
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    result_files[file_type] = len(f.readlines())
        
        export_data = {
            'session_id': session_id,
            'session_info': {
                'connected_at': session_data.get('connected_at', '').isoformat() if isinstance(session_data.get('connected_at'), datetime) else str(session_data.get('connected_at')),
                'mode': session_data.get('mode', 'enhanced_stealth'),
                'client_ip': session_data.get('client_ip', 'unknown'),
                'features': session_data.get('features', [])
            },
            'results_summary': result_files,
            'export_timestamp': datetime.now().isoformat()
        }
        
        return jsonify(export_data)
        
    except Exception as e:
        logger.error(f"Error exporting session data: {e}")
        return jsonify({'error': 'Export failed'}), 500

@app.route('/api/stealth/cleanup/<session_id>')
@limiter.limit("10 per hour")
def cleanup_session(session_id):
    """Clean up session data and files"""
    try:
        if session_id in stealth_sessions:
            # Stop any running checker
            if session_id in stealth_threads:
                stop_stealth_checker(session_id)
                del stealth_threads[session_id]
            
            # Remove session data
            del stealth_sessions[session_id]
            
            # Clean up files
            session_dir = f"sessions/session_{session_id}"
            if os.path.exists(session_dir):
                import shutil
                shutil.rmtree(session_dir)
            
            logger.info(f"🧹 Session {session_id} cleaned up successfully")
            return jsonify({'message': 'Session cleaned up successfully'})
        else:
            return jsonify({'error': 'Session not found'}), 404
            
    except Exception as e:
        logger.error(f"Error cleaning up session: {e}")
        return jsonify({'error': 'Cleanup failed'}), 500

@app.route('/api/debug/parse-combos', methods=['POST'])
@limiter.limit("10 per minute")
def debug_parse_combos():
    """Enhanced debug endpoint with better validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        combo_content = data.get('combo_content', '')
        
        # Enhanced combo parsing with validation
        combos = []
        lines = combo_content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        
        debug_info = {
            'raw_content': combo_content,
            'raw_length': len(combo_content),
            'lines_count': len(lines),
            'lines': [],
            'parsed_combos': [],
            'errors': [],
            'validation_summary': {}
        }
        
        for i, line in enumerate(lines):
            line_info = {
                'line_number': i + 1,
                'raw_line': repr(line),
                'stripped_line': line.strip(),
                'has_colon': ':' in line,
                'parsed': False,
                'validation_errors': []
            }
            
            line = line.strip()
            if line and ':' in line:
                try:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        email, password = parts
                        email = email.strip()
                        password = password.strip()
                        
                        # Enhanced validation
                        validation_errors = []
                        if not email:
                            validation_errors.append("Empty email")
                        elif '@' not in email:
                            validation_errors.append("Invalid email format")
                        elif len(email) > 254:
                            validation_errors.append("Email too long")
                        
                        if not password:
                            validation_errors.append("Empty password")
                        elif len(password) < 1:
                            validation_errors.append("Password too short")
                        
                        if not validation_errors:
                            combos.append((email, password))
                            debug_info['parsed_combos'].append({
                                'line': i + 1,
                                'email': email,
                                'password': '*' * len(password)  # Hide password
                            })
                            line_info['parsed'] = True
                        else:
                            line_info['validation_errors'] = validation_errors
                            debug_info['errors'].extend([f"Line {i + 1}: {', '.join(validation_errors)}"])
                    else:
                        line_info['validation_errors'] = ["Missing colon separator"]
                        debug_info['errors'].append(f"Line {i + 1}: Missing colon separator")
                except Exception as e:
                    line_info['validation_errors'] = [f"Parsing error: {str(e)}"]
                    debug_info['errors'].append(f"Line {i + 1}: {str(e)}")
            
            debug_info['lines'].append(line_info)
        
        # Summary statistics
        debug_info['total_parsed'] = len(combos)
        debug_info['total_errors'] = len(debug_info['errors'])
        debug_info['success_rate'] = f"{(len(combos) / len(lines) * 100):.1f}%" if lines else "0%"
        
        return jsonify(debug_info)
        
    except Exception as e:
        logger.error(f"Error in debug parse combos: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Enhanced 404 error handler"""
    return jsonify({
        'error': 'Endpoint not found',
        'timestamp': datetime.now().isoformat(),
        'version': '3.1.0'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Enhanced 500 error handler"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'timestamp': datetime.now().isoformat(),
        'version': '3.1.0'
    }), 500

@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Rate limit exceeded handler"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'retry_after': error.description,
        'timestamp': datetime.now().isoformat()
    }), 429

def create_directories():
    """Create necessary directories with enhanced structure"""
    directories = ['sessions', 'templates', 'logs', 'exports']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

if __name__ == '__main__':
    create_directories()
    app.start_time = time.time()  # Track app start time for uptime
    
    logger.info("🎮 Xbox Game Pass Ultimate Stealth Validator v3.1.0 starting...")
    logger.info("🥷 Enhanced stealth mode activated - Advanced security & performance!")
    logger.info("🛡️ Rate limiting enabled - 200/day, 50/hour")
    logger.info("📊 Enhanced logging with rotation enabled")
    logger.info("🧹 Automatic session cleanup enabled")
    
    # Use port from environment variable for cloud deployment, default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    try:
        socketio.run(app, host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down enhanced stealth validator...")
    except Exception as e:
        logger.error(f"❌ Error starting enhanced stealth validator: {e}")
