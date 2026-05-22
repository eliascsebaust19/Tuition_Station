import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
import os

def initialize_firebase():
    # Check if already initialized
    if not firebase_admin._apps:
        # Path to your service account key file
        cred_filename = 'tuition-station-firebase-adminsdk-fbsvc-1e70527c43.json'
        cred_path = os.path.join(os.path.dirname(__file__), cred_filename)
        
        if not os.path.exists(cred_path):
            cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')

        # Storage bucket name (usually project-id.appspot.com)
        bucket_name = 'tuition-station.appspot.com'

        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'storageBucket': bucket_name
            })
        else:
            print("Warning: serviceAccountKey.json not found. Firebase features will not work.")
            try:
                firebase_admin.initialize_app()
            except Exception:
                pass

def get_db():
    return firestore.client()

def get_auth():
    return auth

def get_storage():
    return storage
