"""
Enhanced Configuration for Xbox Game Pass Ultimate Stealth Validator
Version: 3.1.0 - Enhanced Security & Performance Edition
"""

import os
from datetime import timedelta

class Config:
    """Main configuration class"""
    
    # Application Settings
    APP_NAME = "Xbox Game Pass Ultimate Stealth Validator"
    APP_VERSION = "3.1.0"
    APP_MODE = "enhanced_stealth_anti_rate_limit"
    
    # Security Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', None)  # Will be auto-generated if not set
    SESSION_LIFETIME = timedelta(hours=24)
    MAX_SESSIONS_PER_IP = 3
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
    # Rate Limiting
    RATE_LIMITS = {
        'default': ["200 per day", "50 per hour"],
        'health_check': "10 per minute",
        'start_check': "5 per minute",
        'download': "30 per hour",
        'export': "20 per hour",
        'cleanup': "10 per hour",
        'debug': "10 per minute"
    }
    
    # Stealth Settings
    STEALTH_DELAY_RANGE = (3, 15)  # seconds
    SESSION_ROTATION_INTERVAL = 25  # requests
    CLEANUP_INTERVAL = 300  # 5 minutes
    
    # Logging Settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # File Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    SUPPORTED_FORMATS = ['.txt', '.csv']
    
    # WebSocket Settings
    SOCKET_PING_TIMEOUT = 60
    SOCKET_PING_INTERVAL = 25
    CORS_ALLOWED_ORIGINS = "*"
    
    # Performance Settings
    THREAD_DAEMON = True
    ZIP_COMPRESSION = True
    
    # Validation Settings
    EMAIL_MAX_LENGTH = 254
    PASSWORD_MIN_LENGTH = 1
    
    # UI Settings
    MOBILE_BREAKPOINT = 768
    NOTIFICATION_TIMEOUT = 5000  # 5 seconds
    PROGRESS_UPDATE_INTERVAL = 30  # seconds
    
    # Export Settings
    EXPORT_TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'
    
    # Error Handling
    MAX_ERROR_LOG_SIZE = 1000
    ERROR_NOTIFICATION_TIMEOUT = 3000  # 3 seconds
    
    # Development Settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    TESTING = os.environ.get('TESTING', 'False').lower() == 'true'
    
    # Cloud Deployment
    PORT = int(os.environ.get('PORT', 5000))
    HOST = '0.0.0.0'
    
    # Feature Flags
    FEATURES = {
        'enhanced_security': True,
        'rate_limiting': True,
        'session_management': True,
        'mobile_responsive': True,
        'progress_tracking': True,
        'error_handling': True,
        'performance_monitoring': True,
        'keyboard_shortcuts': True,
        'auto_cleanup': True,
        'system_metrics': True
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    RATE_LIMITS = {
        'default': ["1000 per day", "100 per hour"],
        'health_check': "100 per minute",
        'start_check': "50 per minute",
        'download': "100 per hour",
        'export': "50 per hour",
        'cleanup': "50 per hour",
        'debug': "100 per minute"
    }

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    
    # Stricter rate limiting for production
    RATE_LIMITS = {
        'default': ["100 per day", "20 per hour"],
        'health_check': "5 per minute",
        'start_check': "2 per minute",
        'download': "10 per hour",
        'export': "5 per hour",
        'cleanup': "2 per hour",
        'debug': "5 per minute"
    }

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    SECRET_KEY = 'test-secret-key'
    
    # Relaxed rate limiting for testing
    RATE_LIMITS = {
        'default': ["10000 per day", "1000 per hour"],
        'health_check': "1000 per minute",
        'start_check': "500 per minute",
        'download': "1000 per hour",
        'export': "500 per hour",
        'cleanup': "500 per hour",
        'debug': "1000 per minute"
    }

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])