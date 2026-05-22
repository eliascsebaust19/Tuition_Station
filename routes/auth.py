import json
import requests
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, TeacherProfile, SubscriptionPlan, UserSubscription
from datetime import datetime, timedelta
from mail_utils import send_welcome_email

auth_bp = Blueprint('auth', __name__)


def redirect_dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.role == 'teacher':
        return redirect(url_for('teacher.dashboard'))
    return redirect(url_for('student.dashboard'))


@auth_bp.route('/')
def index():
    if current_user.is_authenticated and request.args.get('landing') != '1':
        return redirect_dashboard()
    from models import SubscriptionPlan, UserSubscription, Review
    plans = SubscriptionPlan.query.order_by(SubscriptionPlan.price).all()
    teachers = User.query.join(TeacherProfile).filter(
        User.role == 'teacher',
        User.is_approved == True,
        User.is_active == True,
        TeacherProfile.is_complete == True
    ).outerjoin(UserSubscription, db.and_(
        UserSubscription.user_id == User.id,
        UserSubscription.is_active == True
    )).order_by(
        db.case((UserSubscription.plan_id.is_(None), 1), else_=0),
        UserSubscription.plan_id.desc()
    ).limit(12).all()

    teacher_data = []
    for t in teachers:
        profile = TeacherProfile.query.filter_by(user_id=t.id).first()
        sub = UserSubscription.query.filter_by(user_id=t.id, is_active=True).first()
        avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=t.id).scalar() or 0
        review_count = Review.query.filter_by(teacher_id=t.id).count()
        badge = sub.plan.has_verified_badge if sub and sub.plan else False
        featured = sub.plan.is_featured if sub and sub.plan else False
        teacher_data.append({
            'user': t, 'profile': profile, 'avg_rating': round(avg_rating, 1),
            'review_count': review_count, 'verified': badge, 'featured': featured
        })
    return render_template('index.html', teachers=teacher_data, plans=plans)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_dashboard()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.is_active:
                flash('Account blocked. Contact admin.', 'error')
            elif user.role == 'teacher' and not user.is_approved:
                flash('Your account is pending admin approval.', 'warning')
            else:
                login_user(user)
                flash('Welcome back, ' + user.name + '!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or redirect_dashboard())
        else:
            flash('Invalid email or password.', 'error')
    return render_template('auth_new.html', is_login=True)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect_dashboard()
    default_role = request.args.get('role', 'student')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        role = request.form.get('role')

        errors = []
        if not name: errors.append('Name is required.')
        if not email: errors.append('Email is required.')
        if password != confirm: errors.append('Passwords do not match.')
        if len(password) < 6: errors.append('Password must be at least 6 characters.')
        if User.query.filter_by(email=email).first(): errors.append('Email already registered.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('auth_new.html', is_login=False, old=request.form, default_role=default_role)

        try:
            is_approved = role != 'teacher'
            user = User(name=name, email=email, role=role, is_active=True, is_approved=is_approved)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()

            if role == 'teacher':
                profile = TeacherProfile(
                    user_id=user.id,
                    subject=request.form.get('subject', ''),
                    experience=int(request.form.get('experience', 0) or 0),
                    fee=int(request.form.get('fee', 0) or 0),
                    location=request.form.get('location', ''),
                    is_complete=False
                )
                db.session.add(profile)
                free_plan = SubscriptionPlan.query.filter_by(name='Free').first()
                if free_plan:
                    sub = UserSubscription(
                        user_id=user.id, plan_id=free_plan.id,
                        start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=9999),
                        is_active=True
                    )
                    db.session.add(sub)

            db.session.commit()
            send_welcome_email(user)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
    return render_template('auth_new.html', is_login=False, old={}, default_role=default_role)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))


def redirect_dashboard_url():
    if current_user.role == 'admin':
        return url_for('admin.dashboard')
    elif current_user.role == 'teacher':
        return url_for('teacher.dashboard')
    return url_for('student.dashboard')


@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    try:
        data = request.get_json()
        access_token = data.get('access_token')
        role = data.get('role', 'student')
        if not access_token:
            return jsonify({'success': False, 'error': 'No access token provided'}), 400

        resp = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={
            'Authorization': f'Bearer {access_token}'
        })
        if resp.status_code != 200:
            return jsonify({'success': False, 'error': 'Failed to verify Google token'}), 400

        google_data = resp.json()
        email = google_data.get('email')
        name = google_data.get('name', email.split('@')[0])
        picture = google_data.get('picture')

        user = User.query.filter_by(email=email).first()
        if not user:
            import secrets
            is_approved = role != 'teacher'
            user = User(name=name, email=email, role=role, is_active=True, is_approved=is_approved)
            if picture:
                user.profile_picture = picture
            user.set_password(secrets.token_urlsafe(16))
            db.session.add(user)
            db.session.flush()

            if role == 'teacher':
                profile = TeacherProfile(user_id=user.id, subject='', experience=0, fee=0, location='', is_complete=False)
                db.session.add(profile)
                free_plan = SubscriptionPlan.query.filter_by(name='Free').first()
                if free_plan:
                    sub = UserSubscription(user_id=user.id, plan_id=free_plan.id,
                        start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=9999), is_active=True)
                    db.session.add(sub)

            db.session.commit()
            send_welcome_email(user)
        elif picture and not user.profile_picture:
            user.profile_picture = picture
            db.session.commit()

        login_user(user)
        return jsonify({'success': True, 'redirect': redirect_dashboard_url()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@auth_bp.route('/facebook-login', methods=['POST'])
def facebook_login():
    try:
        data = request.get_json()
        id_token = data.get('id_token')
        role = data.get('role', 'student')
        if not id_token:
            return jsonify({'success': False, 'error': 'No ID token provided'}), 400

        resp = requests.get(f'https://graph.facebook.com/me?fields=id,name,email,picture.type(large)&access_token={id_token}')
        if resp.status_code != 200:
            return jsonify({'success': False, 'error': 'Failed to verify Facebook token'}), 400

        fb_data = resp.json()
        email = fb_data.get('email', f'{fb_data["id"]}@facebook.com')
        name = fb_data.get('name', email.split('@')[0])
        picture = fb_data.get('picture', {}).get('data', {}).get('url') if isinstance(fb_data.get('picture'), dict) else None

        user = User.query.filter_by(email=email).first()
        if not user:
            import secrets
            is_approved = role != 'teacher'
            user = User(name=name, email=email, role=role, is_active=True, is_approved=is_approved)
            if picture:
                user.profile_picture = picture
            user.set_password(secrets.token_urlsafe(16))
            db.session.add(user)
            db.session.flush()

            if role == 'teacher':
                profile = TeacherProfile(user_id=user.id, subject='', experience=0, fee=0, location='', is_complete=False)
                db.session.add(profile)
                free_plan = SubscriptionPlan.query.filter_by(name='Free').first()
                if free_plan:
                    sub = UserSubscription(user_id=user.id, plan_id=free_plan.id,
                        start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=9999), is_active=True)
                    db.session.add(sub)

            db.session.commit()
            send_welcome_email(user)
        elif picture and not user.profile_picture:
            user.profile_picture = picture
            db.session.commit()

        login_user(user)
        return jsonify({'success': True, 'redirect': redirect_dashboard_url()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@auth_bp.route('/developer')
def developer():
    return render_template('developer.html')
