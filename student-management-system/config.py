import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Application configuration class."""
    
    # Secret key for CSRF protection and session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # SQLite database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'student_management.db')
    
    # Disable modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Form CSRF enabled
    WTF_CSRF_ENABLED = True
