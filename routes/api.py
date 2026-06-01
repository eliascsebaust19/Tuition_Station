import json
from datetime import datetime, timedelta
from functools import wraps

import requests
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    JWTManager
)
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, TeacherProfile, SubscriptionPlan, UserSubscription, \
    Payment, TuitionPost, Application, Message, Notification, SavedTutor, Review, ToDo, AdminLog

api_bp = Blueprint('api', __name__, url_prefix='/api')


def api_role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.role not in roles:
                return jsonify({'success': False, 'error': 'Access denied'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active,
        'is_approved': user.is_approved,
        'profile_picture': user.profile_picture,
        'created_at': user.created_at.isoformat() if user.created_at else None,
    }


def teacher_profile_to_dict(profile):
    if not profile:
        return None
    return {
        'id': profile.id,
        'user_id': profile.user_id,
        'university': profile.university,
        'department': profile.department,
        'degree': profile.degree,
        'subject': profile.subject,
        'experience': profile.experience,
        'fee': profile.fee,
        'hourly_fee': profile.hourly_fee,
        'location': profile.location,
        'bio': profile.bio,
        'availability': profile.availability,
        'is_complete': profile.is_complete,
        'teaching_mode': profile.teaching_mode,
        'qualification': profile.qualification,
        'subjects_expert_in': profile.subjects_expert_in,
        'class_level': profile.class_level,
        'teaching_areas': profile.teaching_areas,
        'languages': profile.languages,
        'teaching_style': profile.teaching_style,
        'total_students_taught': profile.total_students_taught,
        'intro_video_url': profile.intro_video_url,
        'cv': profile.cv,
    }


# ===================== AUTH ENDPOINTS =====================

@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Request body required'}), 400
    email = data.get('email', '').strip()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password required'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
    if not user.is_active:
        return jsonify({'success': False, 'error': 'Account blocked. Contact admin.'}), 403
    if user.role == 'teacher' and not user.is_approved:
        return jsonify({'success': False, 'error': 'Account pending admin approval.'}), 403
    token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))
    return jsonify({
        'success': True,
        'token': token,
        'user': user_to_dict(user),
    })


@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Request body required'}), 400
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    role = data.get('role', 'student')
    if role not in ('student', 'teacher'):
        return jsonify({'success': False, 'error': 'Role must be student or teacher'}), 400
    if not name or not email or not password:
        return jsonify({'success': False, 'error': 'Name, email, and password required'}), 400
    if len(password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'error': 'Email already registered'}), 409
    try:
        is_approved = role != 'teacher'
        user = User(name=name, email=email, role=role, is_active=True, is_approved=is_approved)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        if role == 'teacher':
            profile = TeacherProfile(
                user_id=user.id, subject='', experience=0, fee=0, location='', is_complete=False
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
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))
        return jsonify({'success': True, 'token': token, 'user': user_to_dict(user)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/auth/google', methods=['POST'])
def api_google_login():
    data = request.get_json()
    access_token = data.get('access_token') if data else None
    role = data.get('role', 'student') if data else 'student'
    if not access_token:
        return jsonify({'success': False, 'error': 'No access token provided'}), 400
    try:
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
        elif picture and not user.profile_picture:
            user.profile_picture = picture
            db.session.commit()
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))
        return jsonify({'success': True, 'token': token, 'user': user_to_dict(user)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def api_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    result = user_to_dict(user)
    if user.role == 'teacher':
        result['profile'] = teacher_profile_to_dict(user.teacher_profile)
        sub = UserSubscription.query.filter_by(user_id=user.id, is_active=True).first()
        if sub:
            result['subscription'] = {
                'plan_name': sub.plan.name if sub.plan else 'Free',
                'is_active': sub.is_active,
                'days_remaining': sub.days_remaining,
            }
        else:
            result['subscription'] = {'plan_name': 'Free', 'is_active': False, 'days_remaining': 0}
        application_count = Application.query.filter_by(teacher_id=user.id).count()
        result['application_count'] = application_count
    if user.role == 'student':
        post_count = TuitionPost.query.filter_by(student_id=user.id).count()
        result['post_count'] = post_count
    unread = Message.query.filter_by(receiver_id=user.id, is_read=False).count()
    result['unread_messages'] = unread
    notif_count = Notification.query.filter_by(user_id=user.id, is_read=False).count()
    result['unread_notifications'] = notif_count
    return jsonify({'success': True, 'data': result})


# ===================== STUDENT ENDPOINTS =====================

@api_bp.route('/students/search', methods=['GET'])
@jwt_required()
def api_search_tutors():
    query = request.args.get('q', '').strip()
    subject = request.args.get('subject', '').strip()
    location = request.args.get('location', '').strip()
    min_fee = request.args.get('min_fee', type=int)
    max_fee = request.args.get('max_fee', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    base = db.session.query(User, TeacherProfile, UserSubscription).join(
        TeacherProfile, TeacherProfile.user_id == User.id
    ).outerjoin(
        UserSubscription, db.and_(
            UserSubscription.user_id == User.id,
            UserSubscription.is_active == True
        )
    ).filter(User.role == 'teacher', User.is_approved == True, User.is_active == True)
    if query:
        pattern = f'%{query}%'
        base = base.filter(
            db.or_(User.name.ilike(pattern), TeacherProfile.subject.ilike(pattern),
                   TeacherProfile.bio.ilike(pattern), TeacherProfile.location.ilike(pattern))
        )
    if subject:
        base = base.filter(TeacherProfile.subject.ilike(f'%{subject}%'))
    if location:
        base = base.filter(TeacherProfile.location.ilike(f'%{location}%'))
    if min_fee is not None:
        base = base.filter(TeacherProfile.fee >= min_fee)
    if max_fee is not None:
        base = base.filter(TeacherProfile.fee <= max_fee)
    base = base.order_by(
        db.case((UserSubscription.plan_id.is_(None), 1), else_=0),
        UserSubscription.plan_id.desc()
    )
    total = base.count()
    results = base.offset((page - 1) * per_page).limit(per_page).all()
    teachers = []
    for u, p, s in results:
        avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=u.id).scalar() or 0
        review_count = Review.query.filter_by(teacher_id=u.id).count()
        badge = s.plan.has_verified_badge if s and s.plan else False
        featured = s.plan.is_featured if s and s.plan else False
        teachers.append({
            'user': user_to_dict(u),
            'profile': teacher_profile_to_dict(p),
            'avg_rating': round(float(avg_rating), 1),
            'review_count': review_count,
            'verified': badge,
            'featured': featured,
        })
    return jsonify({
        'success': True,
        'data': teachers,
        'total': total,
        'page': page,
        'per_page': per_page,
    })


@api_bp.route('/teachers/<int:teacher_id>', methods=['GET'])
@jwt_required()
def api_teacher_detail(teacher_id):
    user = User.query.get(teacher_id)
    if not user or user.role != 'teacher':
        return jsonify({'success': False, 'error': 'Teacher not found'}), 404
    profile = teacher_profile_to_dict(user.teacher_profile)
    avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=user.id).scalar() or 0
    review_count = Review.query.filter_by(teacher_id=user.id).count()
    reviews = Review.query.filter_by(teacher_id=user.id).order_by(Review.created_at.desc()).limit(10).all()
    sub = UserSubscription.query.filter_by(user_id=user.id, is_active=True).first()
    badge = sub.plan.has_verified_badge if sub and sub.plan else False
    return jsonify({
        'success': True,
        'data': {
            'user': user_to_dict(user),
            'profile': profile,
            'avg_rating': round(float(avg_rating), 1),
            'review_count': review_count,
            'verified': badge,
            'reviews': [{
                'id': r.id,
                'rating': r.rating,
                'comment': r.comment,
                'student_name': r.reviewer.name if r.reviewer else 'Anonymous',
                'created_at': r.created_at.isoformat() if r.created_at else None,
            } for r in reviews],
        }
    })


@api_bp.route('/students/tuition-posts', methods=['GET', 'POST'])
@jwt_required()
@api_role_required('student')
def api_tuition_posts():
    user_id = get_jwt_identity()
    if request.method == 'GET':
        posts = TuitionPost.query.filter_by(student_id=user_id).order_by(TuitionPost.created_at.desc()).all()
        return jsonify({'success': True, 'data': [{
            'id': p.id,
            'title': p.title,
            'subject': p.subject,
            'class_level': p.class_level,
            'location': p.location,
            'salary': p.salary,
            'status': p.status,
            'created_at': p.created_at.isoformat() if p.created_at else None,
            'application_count': Application.query.filter_by(post_id=p.id).count(),
        } for p in posts]})
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Request body required'}), 400
    title = data.get('title', '').strip()
    subject = data.get('subject', '').strip()
    location = data.get('location', '').strip()
    if not title or not subject or not location:
        return jsonify({'success': False, 'error': 'Title, subject, and location required'}), 400
    post = TuitionPost(
        student_id=user_id, title=title, subject=subject,
        class_level=data.get('class_level'), location=location,
        salary=data.get('salary', type=int), description=data.get('description'),
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({'success': True, 'data': {'id': post.id}}), 201


@api_bp.route('/students/saved-tutors', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
@api_role_required('student')
def api_saved_tutors():
    user_id = get_jwt_identity()
    if request.method == 'GET':
        saved = SavedTutor.query.filter_by(student_id=user_id).order_by(SavedTutor.created_at.desc()).all()
        results = []
        for s in saved:
            teacher = User.query.get(s.teacher_id)
            if teacher and teacher.teacher_profile:
                avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=teacher.id).scalar() or 0
                results.append({
                    'id': s.id,
                    'teacher': user_to_dict(teacher),
                    'profile': teacher_profile_to_dict(teacher.teacher_profile),
                    'avg_rating': round(float(avg_rating), 1),
                    'created_at': s.created_at.isoformat() if s.created_at else None,
                })
        return jsonify({'success': True, 'data': results})
    data = request.get_json()
    teacher_id = data.get('teacher_id') if data else None
    if not teacher_id:
        return jsonify({'success': False, 'error': 'teacher_id required'}), 400
    if request.method == 'DELETE':
        SavedTutor.query.filter_by(student_id=user_id, teacher_id=teacher_id).delete()
        db.session.commit()
        return jsonify({'success': True})
    existing = SavedTutor.query.filter_by(student_id=user_id, teacher_id=teacher_id).first()
    if existing:
        return jsonify({'success': False, 'error': 'Already saved'}), 409
    saved = SavedTutor(student_id=user_id, teacher_id=teacher_id)
    db.session.add(saved)
    db.session.commit()
    return jsonify({'success': True, 'data': {'id': saved.id}}), 201


@api_bp.route('/reviews', methods=['GET', 'POST'])
@jwt_required()
def api_reviews():
    user_id = get_jwt_identity()
    if request.method == 'GET':
        teacher_id = request.args.get('teacher_id', type=int)
        if teacher_id:
            reviews = Review.query.filter_by(teacher_id=teacher_id).order_by(Review.created_at.desc()).all()
        else:
            reviews = Review.query.filter_by(student_id=user_id).order_by(Review.created_at.desc()).all()
        return jsonify({'success': True, 'data': [{
            'id': r.id,
            'rating': r.rating,
            'comment': r.comment,
            'student_name': r.reviewer.name if r.reviewer else 'Anonymous',
            'teacher_id': r.teacher_id,
            'created_at': r.created_at.isoformat() if r.created_at else None,
        } for r in reviews]})
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Request body required'}), 400
    teacher_id = data.get('teacher_id')
    rating = data.get('rating', type=int)
    if not teacher_id or not rating or rating < 1 or rating > 5:
        return jsonify({'success': False, 'error': 'Valid teacher_id and rating (1-5) required'}), 400
    existing = Review.query.filter_by(student_id=user_id, teacher_id=teacher_id).first()
    if existing:
        return jsonify({'success': False, 'error': 'Already reviewed this teacher'}), 409
    review = Review(student_id=user_id, teacher_id=teacher_id, rating=rating, comment=data.get('comment'))
    db.session.add(review)
    db.session.commit()
    return jsonify({'success': True, 'data': {'id': review.id}}), 201


# ===================== TEACHER ENDPOINTS =====================

@api_bp.route('/teacher/dashboard', methods=['GET'])
@jwt_required()
@api_role_required('teacher')
def api_teacher_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    total_apps = Application.query.filter_by(teacher_id=user_id).count()
    pending_apps = Application.query.filter_by(teacher_id=user_id, status='Pending').count()
    accepted_apps = Application.query.filter_by(teacher_id=user_id, status='Accepted').count()
    open_posts = TuitionPost.query.filter_by(status='Open').count()
    messages = Message.query.filter(
        db.or_(Message.sender_id == user_id, Message.receiver_id == user_id)
    ).count()
    avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=user_id).scalar() or 0
    review_count = Review.query.filter_by(teacher_id=user_id).count()
    sub = UserSubscription.query.filter_by(user_id=user_id, is_active=True).first()
    plan_name = sub.plan.name if sub and sub.plan else 'Free'
    days_remaining = sub.days_remaining if sub else 0
    recent_apps = Application.query.filter_by(teacher_id=user_id).order_by(
        Application.created_at.desc()).limit(5).all()
    return jsonify({
        'success': True,
        'data': {
            'user': user_to_dict(user),
            'profile': teacher_profile_to_dict(user.teacher_profile),
            'stats': {
                'total_applications': total_apps,
                'pending_applications': pending_apps,
                'accepted_applications': accepted_apps,
                'open_posts': open_posts,
                'total_messages': messages,
                'avg_rating': round(float(avg_rating), 1),
                'review_count': review_count,
            },
            'subscription': {
                'plan_name': plan_name,
                'days_remaining': days_remaining,
                'is_active': sub.is_active if sub else False,
            },
            'recent_applications': [{
                'id': a.id,
                'post_title': a.post.title if a.post else 'Unknown',
                'student_name': a.post.student.name if a.post and a.post.student else 'Unknown',
                'status': a.status,
                'created_at': a.created_at.isoformat() if a.created_at else None,
            } for a in recent_apps],
        }
    })


@api_bp.route('/teacher/profile', methods=['GET', 'PUT'])
@jwt_required()
@api_role_required('teacher')
def api_teacher_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    profile = user.teacher_profile
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'data': {
                'user': user_to_dict(user),
                'profile': teacher_profile_to_dict(profile),
            }
        })
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Request body required'}), 400
    if profile:
        for field in ('subject', 'university', 'department', 'degree', 'experience',
                       'fee', 'hourly_fee', 'location', 'bio', 'availability',
                       'teaching_mode', 'qualification', 'subjects_expert_in',
                       'class_level', 'teaching_areas', 'languages', 'teaching_style',
                       'total_students_taught', 'intro_video_url'):
            if field in data:
                setattr(profile, field, data[field])
        profile.is_complete = bool(profile.subject and profile.fee)
        db.session.commit()
    return jsonify({'success': True, 'data': teacher_profile_to_dict(profile)})


@api_bp.route('/teacher/applications', methods=['GET'])
@jwt_required()
@api_role_required('teacher')
def api_teacher_applications():
    user_id = get_jwt_identity()
    status_filter = request.args.get('status', '')
    query = Application.query.filter_by(teacher_id=user_id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    apps = query.order_by(Application.created_at.desc()).all()
    return jsonify({'success': True, 'data': [{
        'id': a.id,
        'post_id': a.post_id,
        'post_title': a.post.title if a.post else 'Unknown',
        'post_subject': a.post.subject if a.post else '',
        'post_location': a.post.location if a.post else '',
        'post_salary': a.post.salary if a.post else 0,
        'student_name': a.post.student.name if a.post and a.post.student else 'Unknown',
        'message': a.message,
        'status': a.status,
        'created_at': a.created_at.isoformat() if a.created_at else None,
    } for a in apps]})


@api_bp.route('/teacher/browse-posts', methods=['GET'])
@jwt_required()
@api_role_required('teacher')
def api_browse_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    subject = request.args.get('subject', '')
    query = TuitionPost.query.filter_by(status='Open')
    if subject:
        query = query.filter(TuitionPost.subject.ilike(f'%{subject}%'))
    total = query.count()
    posts = query.order_by(TuitionPost.created_at.desc()).offset(
        (page - 1) * per_page).limit(per_page).all()
    user_id = get_jwt_identity()
    return jsonify({'success': True, 'data': [{
        'id': p.id,
        'title': p.title,
        'subject': p.subject,
        'class_level': p.class_level,
        'location': p.location,
        'salary': p.salary,
        'description': p.description,
        'student_name': p.student.name if p.student else 'Unknown',
        'has_applied': Application.query.filter_by(post_id=p.id, teacher_id=user_id).first() is not None,
        'created_at': p.created_at.isoformat() if p.created_at else None,
    } for p in posts], 'total': total})


@api_bp.route('/teacher/apply', methods=['POST'])
@jwt_required()
@api_role_required('teacher')
def api_apply_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    post_id = data.get('post_id') if data else None
    if not post_id:
        return jsonify({'success': False, 'error': 'post_id required'}), 400
    post = TuitionPost.query.get(post_id)
    if not post or post.status != 'Open':
        return jsonify({'success': False, 'error': 'Post not found or closed'}), 404
    existing = Application.query.filter_by(post_id=post_id, teacher_id=user_id).first()
    if existing:
        return jsonify({'success': False, 'error': 'Already applied'}), 409
    app = Application(post_id=post_id, teacher_id=user_id, message=data.get('message', ''))
    db.session.add(app)
    notif = Notification(
        user_id=post.student_id, type='application',
        title='New Application Received',
        message=f'A teacher has applied to your tuition post "{post.title}"',
        link=f'/student/posts'
    )
    db.session.add(notif)
    db.session.commit()
    return jsonify({'success': True, 'data': {'id': app.id}}), 201


@api_bp.route('/teacher/analytics', methods=['GET'])
@jwt_required()
@api_role_required('teacher')
def api_teacher_analytics():
    user_id = get_jwt_identity()
    total_apps = Application.query.filter_by(teacher_id=user_id).count()
    pending = Application.query.filter_by(teacher_id=user_id, status='Pending').count()
    accepted = Application.query.filter_by(teacher_id=user_id, status='Accepted').count()
    rejected = Application.query.filter_by(teacher_id=user_id, status='Rejected').count()
    avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=user_id).scalar() or 0
    review_count = Review.query.filter_by(teacher_id=user_id).count()
    return jsonify({
        'success': True,
        'data': {
            'total_applications': total_apps,
            'pending': pending,
            'accepted': accepted,
            'rejected': rejected,
            'avg_rating': round(float(avg_rating), 1),
            'review_count': review_count,
        }
    })


# ===================== ADMIN ENDPOINTS =====================

@api_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@api_role_required('admin')
def api_admin_dashboard():
    total_users = User.query.count()
    total_teachers = User.query.filter_by(role='teacher').count()
    total_students = User.query.filter_by(role='student').count()
    pending_teachers = User.query.filter_by(role='teacher', is_approved=False).count()
    total_posts = TuitionPost.query.count()
    open_posts = TuitionPost.query.filter_by(status='Open').count()
    total_payments = Payment.query.count()
    pending_payments = Payment.query.filter_by(status='Pending').count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status='Verified').scalar() or 0
    return jsonify({
        'success': True,
        'data': {
            'total_users': total_users,
            'total_teachers': total_teachers,
            'total_students': total_students,
            'pending_teachers': pending_teachers,
            'total_posts': total_posts,
            'open_posts': open_posts,
            'total_payments': total_payments,
            'pending_payments': pending_payments,
            'total_revenue': float(total_revenue),
        }
    })


@api_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@api_role_required('admin')
def api_admin_users():
    role = request.args.get('role', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    query = User.query
    if role:
        query = query.filter_by(role=role)
    total = query.count()
    users = query.order_by(User.created_at.desc()).offset(
        (page - 1) * per_page).limit(per_page).all()
    return jsonify({
        'success': True,
        'data': [user_to_dict(u) for u in users],
        'total': total,
        'page': page,
    })


@api_bp.route('/admin/users/<int:user_id>/approve', methods=['POST'])
@jwt_required()
@api_role_required('admin')
def api_approve_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    user.is_approved = True
    db.session.commit()
    return jsonify({'success': True})


@api_bp.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@jwt_required()
@api_role_required('admin')
def api_toggle_user_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({'success': True, 'data': {'is_active': user.is_active}})


@api_bp.route('/admin/payments', methods=['GET'])
@jwt_required()
@api_role_required('admin')
def api_admin_payments():
    status = request.args.get('status', '')
    query = Payment.query
    if status:
        query = query.filter_by(status=status)
    payments = query.order_by(Payment.created_at.desc()).all()
    return jsonify({'success': True, 'data': [{
        'id': p.id,
        'user_name': p.user.name if p.user else 'Unknown',
        'amount': p.amount,
        'method': p.method,
        'transaction_id': p.transaction_id,
        'status': p.status,
        'created_at': p.created_at.isoformat() if p.created_at else None,
    } for p in payments]})


@api_bp.route('/admin/payments/<int:payment_id>/verify', methods=['POST'])
@jwt_required()
@api_role_required('admin')
def api_verify_payment(payment_id):
    admin_id = get_jwt_identity()
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'success': False, 'error': 'Payment not found'}), 404
    payment.status = 'Verified'
    payment.verified_by = admin_id
    payment.verified_at = datetime.utcnow()
    plan = SubscriptionPlan.query.get(payment.plan_id)
    if plan:
        sub = UserSubscription.query.filter_by(user_id=payment.user_id).first()
        if sub:
            sub.plan_id = plan.id
            sub.is_active = True
            sub.end_date = datetime.utcnow() + timedelta(days=plan.duration_days)
        else:
            sub = UserSubscription(
                user_id=payment.user_id, plan_id=plan.id,
                start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=plan.duration_days),
                is_active=True
            )
            db.session.add(sub)
    db.session.commit()
    return jsonify({'success': True})


# ===================== CHAT ENDPOINTS =====================

@api_bp.route('/chat/conversations', methods=['GET'])
@jwt_required()
def api_conversations():
    user_id = get_jwt_identity()
    sent = db.session.query(Message.receiver_id).filter(Message.sender_id == user_id).distinct().subquery()
    received = db.session.query(Message.sender_id).filter(Message.receiver_id == user_id).distinct().subquery()
    user_ids = set()
    for row in db.session.query(sent.c.receiver_id).all():
        user_ids.add(row[0])
    for row in db.session.query(received.c.sender_id).all():
        user_ids.add(row[0])
    conversations = []
    for other_id in user_ids:
        other = User.query.get(other_id)
        if not other:
            continue
        last_msg = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == user_id, Message.receiver_id == other_id),
                db.and_(Message.sender_id == other_id, Message.receiver_id == user_id)
            )
        ).order_by(Message.created_at.desc()).first()
        unread = Message.query.filter_by(sender_id=other_id, receiver_id=user_id, is_read=False).count()
        conversations.append({
            'user': user_to_dict(other),
            'last_message': last_msg.message if last_msg else '',
            'last_message_time': last_msg.created_at.isoformat() if last_msg and last_msg.created_at else None,
            'unread_count': unread,
        })
    conversations.sort(key=lambda c: c['last_message_time'] or '', reverse=True)
    return jsonify({'success': True, 'data': conversations})


@api_bp.route('/chat/messages/<int:other_user_id>', methods=['GET', 'POST'])
@jwt_required()
def api_messages(other_user_id):
    user_id = get_jwt_identity()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        msgs = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == user_id, Message.receiver_id == other_user_id),
                db.and_(Message.sender_id == other_user_id, Message.receiver_id == user_id)
            )
        ).order_by(Message.created_at.desc()).offset(
            (page - 1) * per_page).limit(per_page).all()
        Message.query.filter_by(sender_id=other_user_id, receiver_id=user_id, is_read=False).update(
            {'is_read': True, 'read_at': datetime.utcnow()}
        )
        db.session.commit()
        return jsonify({'success': True, 'data': [{
            'id': m.id,
            'sender_id': m.sender_id,
            'receiver_id': m.receiver_id,
            'message': m.message,
            'is_read': m.is_read,
            'created_at': m.created_at.isoformat() if m.created_at else None,
        } for m in reversed(msgs)]})
    data = request.get_json()
    if not data or not data.get('message'):
        return jsonify({'success': False, 'error': 'Message required'}), 400
    msg = Message(sender_id=user_id, receiver_id=other_user_id, message=data['message'])
    db.session.add(msg)
    notif = Notification(
        user_id=other_user_id, type='message',
        title='New Message',
        message=data['message'][:100],
        link='/chat'
    )
    db.session.add(notif)
    db.session.commit()
    return jsonify({'success': True, 'data': {
        'id': msg.id,
        'created_at': msg.created_at.isoformat() if msg.created_at else None,
    }}), 201


# ===================== NOTIFICATIONS =====================

@api_bp.route('/notifications', methods=['GET'])
@jwt_required()
def api_notifications():
    user_id = get_jwt_identity()
    notifs = Notification.query.filter_by(user_id=user_id).order_by(
        Notification.created_at.desc()).limit(50).all()
    return jsonify({'success': True, 'data': [{
        'id': n.id,
        'type': n.type,
        'title': n.title,
        'message': n.message,
        'link': n.link,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat() if n.created_at else None,
    } for n in notifs]})


@api_bp.route('/notifications/<int:notif_id>/read', methods=['POST'])
@jwt_required()
def api_read_notification(notif_id):
    user_id = get_jwt_identity()
    notif = Notification.query.filter_by(id=notif_id, user_id=user_id).first()
    if not notif:
        return jsonify({'success': False, 'error': 'Notification not found'}), 404
    notif.is_read = True
    db.session.commit()
    return jsonify({'success': True})


# ===================== SUBSCRIPTIONS =====================

@api_bp.route('/subscriptions/plans', methods=['GET'])
@jwt_required()
def api_subscription_plans():
    plans = SubscriptionPlan.query.order_by(SubscriptionPlan.price).all()
    return jsonify({'success': True, 'data': [{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'duration_days': p.duration_days,
        'max_applications': p.max_applications,
        'is_featured': p.is_featured,
        'has_verified_badge': p.has_verified_badge,
        'priority_ranking': p.priority_ranking,
        'description': p.description,
    } for p in plans]})


@api_bp.route('/subscriptions/my', methods=['GET'])
@jwt_required()
def api_my_subscription():
    user_id = get_jwt_identity()
    sub = UserSubscription.query.filter_by(user_id=user_id, is_active=True).first()
    if not sub:
        return jsonify({'success': True, 'data': None})
    return jsonify({'success': True, 'data': {
        'id': sub.id,
        'plan_id': sub.plan_id,
        'plan_name': sub.plan.name if sub.plan else 'Free',
        'price': sub.plan.price if sub.plan else 0,
        'start_date': sub.start_date.isoformat() if sub.start_date else None,
        'end_date': sub.end_date.isoformat() if sub.end_date else None,
        'days_remaining': sub.days_remaining,
        'is_active': sub.is_active,
        'auto_renew': sub.auto_renew,
    }})


# ===================== PAYMENTS =====================

@api_bp.route('/payments', methods=['GET', 'POST'])
@jwt_required()
def api_payments():
    user_id = get_jwt_identity()
    if request.method == 'GET':
        payments = Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc()).all()
        return jsonify({'success': True, 'data': [{
            'id': p.id,
            'plan_name': p.plan_ref.name if p.plan_ref else 'Unknown',
            'amount': p.amount,
            'method': p.method,
            'transaction_id': p.transaction_id,
            'status': p.status,
            'created_at': p.created_at.isoformat() if p.created_at else None,
        } for p in payments]})
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Request body required'}), 400
    plan_id = data.get('plan_id')
    method = data.get('method', 'bKash')
    sender_number = data.get('sender_number', '')
    transaction_id = data.get('transaction_id', '')
    if not plan_id or not transaction_id:
        return jsonify({'success': False, 'error': 'plan_id and transaction_id required'}), 400
    plan = SubscriptionPlan.query.get(plan_id)
    if not plan:
        return jsonify({'success': False, 'error': 'Plan not found'}), 404
    payment = Payment(
        user_id=user_id, plan_id=plan_id, amount=plan.price,
        method=method, sender_number=sender_number,
        transaction_id=transaction_id, status='Pending'
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'success': True, 'data': {'id': payment.id}}), 201


# ===================== TODO =====================

@api_bp.route('/todos', methods=['GET', 'POST'])
@jwt_required()
def api_todos():
    user_id = get_jwt_identity()
    if request.method == 'GET':
        todos = ToDo.query.filter_by(user_id=user_id).order_by(ToDo.created_at.desc()).all()
        return jsonify({'success': True, 'data': [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'is_completed': t.is_completed,
            'created_at': t.created_at.isoformat() if t.created_at else None,
        } for t in todos]})
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'success': False, 'error': 'Title required'}), 400
    todo = ToDo(user_id=user_id, title=data['title'], description=data.get('description'))
    db.session.add(todo)
    db.session.commit()
    return jsonify({'success': True, 'data': {'id': todo.id}}), 201


@api_bp.route('/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def api_todo_item(todo_id):
    user_id = get_jwt_identity()
    todo = ToDo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return jsonify({'success': False, 'error': 'Todo not found'}), 404
    if request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'success': True})
    data = request.get_json()
    if data:
        if 'title' in data:
            todo.title = data['title']
        if 'description' in data:
            todo.description = data['description']
        if 'is_completed' in data:
            todo.is_completed = data['is_completed']
    db.session.commit()
    return jsonify({'success': True})


# ===================== FEATURED / LANDING =====================

@api_bp.route('/featured-teachers', methods=['GET'])
def api_featured_teachers():
    teachers = db.session.query(User, TeacherProfile, UserSubscription).join(
        TeacherProfile, TeacherProfile.user_id == User.id
    ).outerjoin(
        UserSubscription, db.and_(
            UserSubscription.user_id == User.id,
            UserSubscription.is_active == True
        )
    ).filter(
        User.role == 'teacher', User.is_approved == True, User.is_active == True,
        TeacherProfile.is_complete == True
    ).order_by(
        db.case((UserSubscription.plan_id.is_(None), 1), else_=0),
        UserSubscription.plan_id.desc()
    ).limit(12).all()
    results = []
    for u, p, s in teachers:
        avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=u.id).scalar() or 0
        review_count = Review.query.filter_by(teacher_id=u.id).count()
        badge = s.plan.has_verified_badge if s and s.plan else False
        results.append({
            'user': user_to_dict(u),
            'profile': teacher_profile_to_dict(p),
            'avg_rating': round(float(avg_rating), 1),
            'review_count': review_count,
            'verified': badge,
        })
    return jsonify({'success': True, 'data': results})
