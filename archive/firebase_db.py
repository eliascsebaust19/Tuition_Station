
import requests
from firebase_config import get_db, get_auth, get_storage, initialize_firebase
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

initialize_firebase()

db = get_db()
firebase_auth = get_auth()
storage = get_storage()


class FirebaseUser(UserMixin):
    def __init__(self, user_id, data):
        self.id = user_id
        self.name = data.get('name')
        self.email = data.get('email')
        self.role = data.get('role')
        self._is_active = data.get('is_active', True)
        self.is_approved = data.get('is_approved', False)
        self.is_online = data.get('is_online', False)
        self.profile_picture = data.get('profile_picture')
        self.created_at = data.get('created_at')
        self.password_hash = data.get('password_hash')

    @property
    def is_active(self):
        return self._is_active

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_id(user_id):
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            return FirebaseUser(user_id, user_doc.to_dict())
        return None

    @staticmethod
    def get_by_email(email):
        users = db.collection('users').where(filter=FieldFilter('email', '==', email)).limit(1).get()
        for user in users:
            return FirebaseUser(user.id, user.to_dict())
        return None

    @staticmethod
    def verify_firebase_token(id_token):
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None

    @staticmethod
    def create(name, email, password, role, **kwargs):
        try:
            user_record = firebase_auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            user_id = user_record.uid
        except Exception as e:
            print(f"Error creating user: {e}")
            try:
                user_record = firebase_auth.get_user_by_email(email)
                user_id = user_record.uid
            except:
                raise e

        user_data = {
            'name': name,
            'email': email,
            'role': role,
            'is_active': kwargs.get('is_active', True),
            'is_approved': kwargs.get('is_approved', False),
            'is_online': False,
            'profile_picture': kwargs.get('profile_picture'),
            'created_at': datetime.utcnow()
        }
        db.collection('users').document(user_id).set(user_data)
        return user_id

    def update(self, data):
        db.collection('users').document(self.id).update(data)

    @staticmethod
    def count(role=None, **kwargs):
        query = db.collection('users')
        if role:
            query = query.where(filter=FieldFilter('role', '==', role))
        for key, value in kwargs.items():
            query = query.where(filter=FieldFilter(key, '==', value))
        try:
            return query.count().get()[0][0].value
        except (AttributeError, Exception):
            return len(query.get())


class FirebaseTeacherProfile:
    @staticmethod
    def get_by_user_id(user_id):
        profiles = db.collection('teacher_profiles').where(filter=FieldFilter('user_id', '==', user_id)).limit(1).get()
        for profile in profiles:
            return profile.id, profile.to_dict()
        return None, None

    @staticmethod
    def create(user_id, data):
        data['user_id'] = user_id
        data['created_at'] = datetime.utcnow()
        if 'availability' not in data:
            data['availability'] = 'Available'
        doc_ref = db.collection('teacher_profiles').add(data)
        return doc_ref[1].id

    @staticmethod
    def get_featured(limit=6):
        profiles_docs = db.collection('teacher_profiles').where(filter=FieldFilter('is_complete', '==', True)).limit(limit * 2).get()
        user_ids = [p.to_dict()['user_id'] for p in profiles_docs]
        if not user_ids:
            return []
        user_refs = [db.collection('users').document(uid) for uid in user_ids[:30]]
        users_docs = db.get_all(user_refs)
        users_dict = {u.id: FirebaseUser(u.id, u.to_dict()) for u in users_docs if u.exists}
        results = []
        for p in profiles_docs:
            p_data = p.to_dict()
            user = users_dict.get(p_data['user_id'])
            if user and user.role == 'teacher' and user.is_active and user.is_approved:
                results.append({'profile': p_data, 'user': user})
                if len(results) >= limit:
                    break
        return results

    @staticmethod
    def get_available(limit=8):
        profiles_docs = db.collection('teacher_profiles').where(filter=FieldFilter('availability', '==', 'Available')).limit(limit * 2).get()
        user_ids = [p.to_dict()['user_id'] for p in profiles_docs]
        if not user_ids:
            return []
        user_refs = [db.collection('users').document(uid) for uid in user_ids[:30]]
        users_docs = db.get_all(user_refs)
        users_dict = {u.id: FirebaseUser(u.id, u.to_dict()) for u in users_docs if u.exists}
        results = []
        for p in profiles_docs:
            p_data = p.to_dict()
            user = users_dict.get(p_data['user_id'])
            if user and user.role == 'teacher' and user.is_active and user.is_approved:
                results.append({'profile': p_data, 'user': user})
                if len(results) >= limit:
                    break
        return results

    @staticmethod
    def update(profile_id, data):
        db.collection('teacher_profiles').document(profile_id).update(data)


class FirebaseToDo:
    @staticmethod
    def get_by_user_id(user_id):
        todos_docs = db.collection('todos').where(filter=FieldFilter('user_id', '==', user_id)).get()
        todos = [{'id': t.id, **t.to_dict()} for t in todos_docs]
        return sorted(todos, key=lambda x: x.get('created_at') or datetime.min, reverse=True)

    @staticmethod
    def create(user_id, title, description=None):
        data = {
            'user_id': user_id,
            'title': title,
            'description': description,
            'is_completed': False,
            'created_at': datetime.utcnow()
        }
        doc_ref = db.collection('todos').add(data)
        return doc_ref[1].id

    @staticmethod
    def update(todo_id, data):
        db.collection('todos').document(todo_id).update(data)

    @staticmethod
    def delete(todo_id):
        db.collection('todos').document(todo_id).delete()


class FirebaseTuitionRequest:
    @staticmethod
    def create(student_id, teacher_id, message):
        data = {
            'student_id': student_id,
            'teacher_id': teacher_id,
            'message': message,
            'status': 'pending',
            'created_at': datetime.utcnow()
        }
        doc_ref = db.collection('tuition_requests').add(data)
        return doc_ref[1].id


class FirebaseSavedTutor:
    @staticmethod
    def save(student_id, tutor_id):
        existing = db.collection('saved_tutors')\
            .where(filter=FieldFilter('student_id', '==', student_id))\
            .where(filter=FieldFilter('tutor_id', '==', tutor_id))\
            .limit(1).get()
        if len(list(existing)) > 0:
            return False
        data = {
            'student_id': student_id,
            'tutor_id': tutor_id,
            'created_at': datetime.utcnow()
        }
        db.collection('saved_tutors').add(data)
        return True


class FirebaseMessage:
    @staticmethod
    def send(sender_id, receiver_id, message_text):
        data = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message': message_text,
            'is_read': False,
            'created_at': datetime.utcnow()
        }
        doc_ref = db.collection('messages').add(data)
        return doc_ref[1].id


class FirebaseReview:
    @staticmethod
    def create(student_id, teacher_id, rating, comment):
        data = {
            'student_id': student_id,
            'teacher_id': teacher_id,
            'rating': int(rating),
            'comment': comment,
            'created_at': datetime.utcnow()
        }
        doc_ref = db.collection('reviews').add(data)
        return doc_ref[1].id
