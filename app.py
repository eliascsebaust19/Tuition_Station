from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from firebase_config import initialize_firebase

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def seed_database():
    from models import SubscriptionPlan, UserSubscription, TeacherProfile
    from datetime import datetime, timedelta

    try:
        import sqlalchemy as sa
        db.create_all()
        print("Tables ensured in SQL Server")
    except Exception as e:
        print(f"Note: Database table creation deferred: {e}")
        print("Run schema.sql first, then restart the app.")
        return

    if SubscriptionPlan.query.count() == 0:
        plans = [
            SubscriptionPlan(name='Free', price=0, duration_days=9999, max_applications=3,
                             is_featured=False, has_verified_badge=False, priority_ranking=0,
                             description='Get started with basic access. Apply to 3 tuition posts per month.'),
            SubscriptionPlan(name='Standard', price=499, duration_days=30, max_applications=None,
                             is_featured=False, has_verified_badge=True, priority_ranking=1,
                             description='Unlimited applications, verified profile badge, and priority search ranking.'),
            SubscriptionPlan(name='Premium', price=999, duration_days=30, max_applications=None,
                             is_featured=True, has_verified_badge=True, priority_ranking=2,
                             description='Everything in Standard plus homepage featured placement, analytics dashboard, and priority support.'),
        ]
        db.session.add_all(plans)
        db.session.commit()
        print("Subscription plans created")

    admin = User.query.filter_by(email='admin@tuition.com').first()
    if not admin:
        admin = User(name='Admin', email='admin@tuition.com', role='admin', is_active=True, is_approved=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin created: admin@tuition.com / admin123")

    existing_emails = {u.email for u in User.query.filter_by(role='teacher').all()}
    all_teachers = [
        {'name': 'Dr. Ahmed Hassan', 'email': 'ahmed@tutor.com', 'subject': 'Mathematics', 'experience': 10, 'fee': 5000, 'location': 'Dhanmondi, Dhaka', 'bio': 'PhD in Mathematics with 10 years of teaching experience.'},
        {'name': 'Sarah Rahman', 'email': 'sarah@tutor.com', 'subject': 'English', 'experience': 7, 'fee': 4000, 'location': 'Gulshan, Dhaka', 'bio': 'Native English speaker with expertise in grammar.'},
        {'name': 'Mohammad Khan', 'email': 'khan@tutor.com', 'subject': 'Physics', 'experience': 8, 'fee': 5500, 'location': 'Mirpur, Dhaka', 'bio': 'Experienced physics teacher for SSC and HSC.'},
        {'name': 'Fatima Begum', 'email': 'fatima@tutor.com', 'subject': 'Chemistry', 'experience': 6, 'fee': 4500, 'location': 'Uttara, Dhaka', 'bio': 'Chemistry specialist with practical lab experience.'},
        {'name': 'Abu Bakar', 'email': 'abubakar@tutor.com', 'subject': 'Biology', 'experience': 9, 'fee': 4800, 'location': 'Banani, Dhaka', 'bio': 'Medical graduate teaching biology for HSC.'},
        {'name': 'Lisa Ahmed', 'email': 'lisa@tutor.com', 'subject': 'Class 1-5', 'experience': 5, 'fee': 3000, 'location': 'Baridhara, Dhaka', 'bio': 'Patient teacher specialized in primary education.'},
        {'name': 'Tanvir Hasan', 'email': 'tanvir@tutor.com', 'subject': 'Bangla', 'experience': 6, 'fee': 3500, 'location': 'Mohammadpur, Dhaka', 'bio': 'Bangla literature expert with creative teaching methods.'},
        {'name': 'Nusrat Jahan', 'email': 'nusrat@tutor.com', 'subject': 'English', 'experience': 8, 'fee': 4500, 'location': 'Shyamoli, Dhaka', 'bio': 'IELTS and English grammar specialist.'},
        {'name': 'Rafiq Uddin', 'email': 'rafiq@tutor.com', 'subject': 'Mathematics', 'experience': 12, 'fee': 6000, 'location': 'Khilgaon, Dhaka', 'bio': 'Experienced math teacher for admission test prep.'},
        {'name': 'Shamima Akter', 'email': 'shamima@tutor.com', 'subject': 'Science', 'experience': 5, 'fee': 3200, 'location': 'Badda, Dhaka', 'bio': 'Primary and secondary science teacher.'},
        {'name': 'Kabir Hossain', 'email': 'kabir@tutor.com', 'subject': 'Physics', 'experience': 7, 'fee': 5000, 'location': 'Rampura, Dhaka', 'bio': 'Engineering graduate teaching physics for HSC and admission.'},
        {'name': 'Maliha Tabassum', 'email': 'maliha@tutor.com', 'subject': 'Chemistry', 'experience': 9, 'fee': 5200, 'location': 'Bashundhara, Dhaka', 'bio': 'Chemistry researcher with practical lab-based teaching.'},
    ]
    new_teachers = [t for t in all_teachers if t['email'] not in existing_emails]
    for idx, t in enumerate(new_teachers):
        demo_pic = f"/static/Assets/Image/DemoTeacher{((idx + len(existing_emails)) % 5) + 1}.png"
        user = User(name=t['name'], email=t['email'], role='teacher', is_active=True, is_approved=True, profile_picture=demo_pic)
        user.set_password('password123')
        db.session.add(user)
        db.session.flush()
        profile = TeacherProfile(user_id=user.id, subject=t['subject'], university='University of Dhaka',
            department='Department of ' + t['subject'], degree='BSc', experience=t['experience'],
            fee=t['fee'], location=t['location'], bio=t['bio'], availability='Available', is_complete=True)
        db.session.add(profile)
        free_plan = SubscriptionPlan.query.filter_by(name='Free').first()
        if free_plan:
            sub = UserSubscription(user_id=user.id, plan_id=free_plan.id,
                start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=9999), is_active=True)
            db.session.add(sub)
    if new_teachers:
        db.session.commit()
        print(f"{len(new_teachers)} new sample teachers created with Free subscriptions")
    else:
        print("All sample teachers already exist")

    if User.query.filter_by(role='student').count() == 0:
        sample_students = [
            {'name': 'Rahim Miya', 'email': 'rahim@student.com'},
            {'name': 'Karim Ahmed', 'email': 'karim@student.com'},
        ]
        for s in sample_students:
            user = User(name=s['name'], email=s['email'], role='student', is_active=True, is_approved=True)
            user.set_password('password123')
            db.session.add(user)
        db.session.commit()
        print("Sample students created")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    initialize_firebase()

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_globals():
        from flask import request
        return dict(request=request)

    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.teacher import teacher_bp
    from routes.admin import admin_bp
    from routes.todo import todo_bp
    from routes.subscriptions import subscriptions_bp
    from routes.payments import payments_bp
    from routes.chat import chat_bp
    from routes.bkash import bkash_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(todo_bp, url_prefix='/todo')
    app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(bkash_bp)

    with app.app_context():
        seed_database()

    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import render_template
        return render_template('errors/500.html'), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
