import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tuition-secret-key-2024'
    FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY')
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
    FIREBASE_STORAGE_BUCKET = os.environ.get('FIREBASE_STORAGE_BUCKET')
    FIREBASE_APP_ID = os.environ.get('FIREBASE_APP_ID')
    
    # SQL Server (SSMS) connection - update as needed
    # Format: mssql+pyodbc://username:password@host:port/database?driver=ODBC+Driver+17+for+SQL+Server
    # Windows Auth: mssql+pyodbc://host/database?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mssql+pyodbc://localhost/tuition_system?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BKASH_APP_KEY = os.environ.get('BKASH_APP_KEY', '')
    BKASH_APP_SECRET = os.environ.get('BKASH_APP_SECRET', '')
    BKASH_USERNAME = os.environ.get('BKASH_USERNAME', '')
    BKASH_PASSWORD = os.environ.get('BKASH_PASSWORD', '')
    BKASH_BASE_URL = os.environ.get('BKASH_BASE_URL', 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized')
    BKASH_MERCHANT_NUMBER = os.environ.get('BKASH_MERCHANT_NUMBER', '01XXXXXXXXX')
    BKASH_CALLBACK_URL = os.environ.get('BKASH_CALLBACK_URL', 'http://localhost:5000/bkash/callback')

    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', '')
    FROM_NAME = os.environ.get('FROM_NAME', 'TuitionStation')
    BCC_EMAIL = os.environ.get('BCC_EMAIL', '')
