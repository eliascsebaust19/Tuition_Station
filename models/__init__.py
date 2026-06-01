from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    is_online = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teacher_profile = db.relationship('TeacherProfile', backref='user', uselist=False, lazy=True)
    subscription = db.relationship('UserSubscription', backref='user', uselist=False, lazy=True)
    tuition_posts = db.relationship('TuitionPost', backref='student', lazy=True)
    applications = db.relationship('Application', backref='teacher', lazy=True)
    payments = db.relationship('Payment', foreign_keys='Payment.user_id', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    todos = db.relationship('ToDo', backref='user', lazy=True)
    saved_tutors = db.relationship('SavedTutor', foreign_keys='SavedTutor.student_id', backref='student', lazy=True)
    saved_by = db.relationship('SavedTutor', foreign_keys='SavedTutor.teacher_id', backref='teacher', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TeacherProfile(db.Model):
    __tablename__ = 'teacher_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    university = db.Column(db.String(200))
    department = db.Column(db.String(100))
    degree = db.Column(db.String(50))
    graduation_year = db.Column(db.Integer)
    masters_university = db.Column(db.String(200))
    masters_department = db.Column(db.String(100))
    masters_year = db.Column(db.Integer)
    subject = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, default=0)
    fee = db.Column(db.Integer, nullable=False)
    hourly_fee = db.Column(db.Integer)
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)
    availability = db.Column(db.String(50), default='Available')
    is_complete = db.Column(db.Boolean, default=False)
    cv = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    qualification = db.Column(db.Text)
    subjects_expert_in = db.Column(db.Text)
    class_level = db.Column(db.String(100))
    teaching_areas = db.Column(db.Text)
    teaching_mode = db.Column(db.String(20), default='both')
    demo_class_available = db.Column(db.Boolean, default=False)
    total_students_taught = db.Column(db.Integer, default=0)
    success_percentage = db.Column(db.Integer)
    languages = db.Column(db.String(200))
    teaching_style = db.Column(db.Text)
    availability_schedule = db.Column(db.Text)
    social_links = db.Column(db.Text)
    intro_video_url = db.Column(db.String(500))
    notes_resources = db.Column(db.Text)
    key_strengths = db.Column(db.Text)
    why_students_notice = db.Column(db.Text)
    tuition_experience = db.Column(db.Text)
    reasons_to_hire = db.Column(db.Text)
    preface = db.Column(db.Text)


class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, default=30)
    max_applications = db.Column(db.Integer, nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    has_verified_badge = db.Column(db.Boolean, default=False)
    priority_ranking = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subscriptions = db.relationship('UserSubscription', backref='plan', lazy=True)

    def applications_remaining(self, user_id):
        if self.max_applications is None:
            return None
        from models import Application
        count = Application.query.join(TuitionPost).filter(
            Application.teacher_id == user_id,
            TuitionPost.status == 'Open',
            Application.created_at >= datetime.utcnow().replace(day=1)
        ).count()
        return max(0, self.max_applications - count)


class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    auto_renew = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def days_remaining(self):
        delta = self.end_date - datetime.utcnow()
        return max(0, delta.days)

    @property
    def is_expired(self):
        return self.end_date < datetime.utcnow()

    @property
    def is_expiring_soon(self):
        return 0 < self.days_remaining <= 7


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(20), nullable=False)
    sender_number = db.Column(db.String(20))
    transaction_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    admin_note = db.Column(db.Text)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    plan_ref = db.relationship('SubscriptionPlan', backref='payments', lazy=True)


class TuitionPost(db.Model):
    __tablename__ = 'tuition_posts'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(50))
    location = db.Column(db.String(200), nullable=False)
    salary = db.Column(db.Integer)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='post', lazy=True)


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('tuition_posts.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Message(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {'implicit_returning': False}

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), default='general')
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(500))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SavedTutor(db.Model):
    __tablename__ = 'saved_tutors'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviewer = db.relationship('User', foreign_keys=[student_id], backref='reviews_given')
    teacher_reviewer = db.relationship('User', foreign_keys=[teacher_id], backref='reviews_received')


class ToDo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdminLog(db.Model):
    __tablename__ = 'admin_logs'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
