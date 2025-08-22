#!/usr/bin/env python3
"""
Enhanced Startup Script for Xbox Game Pass Ultimate Stealth Validator
Version: 3.1.0 - Enhanced Security & Performance Edition
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print the enhanced banner"""
    print("🎮" * 50)
    print("🎮 Xbox Game Pass Ultimate Stealth Validator v3.1.0 🎮")
    print("🎮 Enhanced Security & Performance Edition 🎮")
    print("🎮" * 50)
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask>=3.0.0',
        'flask-socketio>=5.3.0', 
        'flask-limiter>=3.5.0',
        'requests>=2.31.0',
        'psutil>=5.9.0'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        package_name = package.split('>=')[0]
        try:
            __import__(package_name.replace('-', '_'))
            print(f"✅ {package_name}")
        except ImportError:
            missing_packages.append(package_name)
            print(f"❌ {package_name}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False
    
    print("✅ All dependencies are satisfied!")
    return True

def setup_environment():
    """Setup environment variables"""
    print("\n🔧 Setting up environment...")
    
    # Set default environment
    if 'FLASK_ENV' not in os.environ:
        os.environ['FLASK_ENV'] = 'development'
        print("✅ FLASK_ENV set to 'development'")
    
    # Set log level
    if 'LOG_LEVEL' not in os.environ:
        os.environ['LOG_LEVEL'] = 'INFO'
        print("✅ LOG_LEVEL set to 'INFO'")
    
    # Generate secret key if not set
    if 'SECRET_KEY' not in os.environ:
        import secrets
        os.environ['SECRET_KEY'] = secrets.token_hex(32)
        print("✅ SECRET_KEY auto-generated")
    
    print(f"✅ Environment: {os.environ['FLASK_ENV']}")
    print(f"✅ Log Level: {os.environ['LOG_LEVEL']}")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['sessions', 'templates', 'logs', 'exports']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_config():
    """Check configuration file"""
    print("\n⚙️ Checking configuration...")
    
    if Path('config.py').exists():
        print("✅ Configuration file found")
    else:
        print("⚠️ Configuration file not found, using defaults")

def start_application():
    """Start the enhanced application"""
    print("\n🚀 Starting Enhanced Stealth Validator...")
    print("🎯 Features enabled:")
    print("   🔐 Rate limiting and session management")
    print("   🛡️ Enhanced security features")
    print("   📱 Mobile responsive design")
    print("   ⌨️ Keyboard shortcuts")
    print("   📊 System monitoring")
    print("   🔔 Enhanced notifications")
    print("   🧹 Auto-cleanup features")
    print("   📈 Progress animations")
    
    print("\n🌐 Dashboard will be available at: http://localhost:5000")
    print("⌨️ Keyboard shortcuts: Ctrl+S (Start), Ctrl+P (Pause), Ctrl+X (Stop)")
    print("\n" + "="*60)
    
    try:
        # Import and run the enhanced application
        from app_stealth import app, socketio
        
        # Set app start time for uptime tracking
        app.start_time = time.time()
        
        # Get port from environment or config
        port = int(os.environ.get('PORT', 5000))
        
        print(f"🎮 Starting on port {port}...")
        socketio.run(app, host='0.0.0.0', port=port, debug=False)
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down enhanced stealth validator...")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Setup environment
    setup_environment()
    
    # Create directories
    create_directories()
    
    # Check configuration
    check_config()
    
    # Start application
    if start_application():
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())