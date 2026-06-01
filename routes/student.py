from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from models import db, User, TeacherProfile, SubscriptionPlan, UserSubscription, TuitionPost, Application, Message, Notification, Review, SavedTutor, ToDo
from datetime import datetime
from routes.utils import role_required, save_uploaded_file

student_bp = Blueprint('student', __name__)
student_required = role_required('student')


@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    my_requests = db.session.query(TuitionPost, Application).join(
        Application, Application.post_id == TuitionPost.id
    ).filter(TuitionPost.student_id == current_user.id).all()

    open_posts = TuitionPost.query.filter_by(student_id=current_user.id, status='Open').count()
    total_posts = TuitionPost.query.filter_by(student_id=current_user.id).count()
    unread_messages = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    tutors = db.session.query(User, TeacherProfile, UserSubscription).join(
        TeacherProfile, TeacherProfile.user_id == User.id
    ).outerjoin(
        UserSubscription, db.and_(
            UserSubscription.user_id == User.id,
            UserSubscription.is_active == True
        )
    ).filter(
        User.role == 'teacher', User.is_approved == True, User.is_active == True,
        TeacherProfile.is_complete == True, TeacherProfile.availability == 'Available'
    ).order_by(
        db.case((UserSubscription.plan_id.is_(None), 1), else_=0),
        UserSubscription.plan_id.desc(),
        TeacherProfile.experience.desc()
    ).limit(12).all()

    tutor_list = []
    for u, p, s in tutors:
        avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=u.id).scalar() or 0
        review_count = Review.query.filter_by(teacher_id=u.id).count()
        plan_name = s.plan.name if s and s.plan else 'Free'
        badge = s.plan.has_verified_badge if s and s.plan else False
        featured = s.plan.is_featured if s and s.plan else False
        tutor_list.append({'user': u, 'profile': p, 'avg_rating': round(avg_rating, 1),
                          'review_count': review_count, 'plan': plan_name,
                          'verified': badge, 'featured': featured})

    todos = ToDo.query.filter_by(user_id=current_user.id, is_completed=False).all()
    return render_template('student/dashboard.html',
        requests=my_requests, open_posts=open_posts, total_posts=total_posts,
        unread_messages=unread_messages, notifications=notifications,
        tutors=tutor_list, todos=todos)


@student_bp.route('/search')
@login_required
@student_required
def search():
    subject = request.args.get('subject', '')
    location = request.args.get('location', '')
    max_fee = request.args.get('max_fee', type=int)
    exp_level = request.args.get('exp_level', '')

    query = db.session.query(User, TeacherProfile, UserSubscription).join(
        TeacherProfile, TeacherProfile.user_id == User.id
    ).outerjoin(
        UserSubscription, db.and_(
            UserSubscription.user_id == User.id,
            UserSubscription.is_active == True
        )
    ).filter(
        User.role == 'teacher', User.is_approved == True, User.is_active == True,
        TeacherProfile.is_complete == True
    )

    if subject:
        query = query.filter(TeacherProfile.subject.ilike(f'%{subject}%'))
    if location:
        query = query.filter(TeacherProfile.location.ilike(f'%{location}%'))
    if max_fee:
        query = query.filter(TeacherProfile.fee <= max_fee)
    if exp_level:
        if exp_level == 'beginner':
            query = query.filter(TeacherProfile.experience < 4)
        elif exp_level == 'intermediate':
            query = query.filter(TeacherProfile.experience.between(4, 7))
        elif exp_level == 'expert':
            query = query.filter(TeacherProfile.experience >= 8)

    query = query.order_by(db.case((UserSubscription.plan_id.is_(None), 1), else_=0), UserSubscription.plan_id.desc(), TeacherProfile.experience.desc())
    results = query.all()

    all_tutors = []
    for u, p, s in results:
        avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=u.id).scalar() or 0
        review_count = Review.query.filter_by(teacher_id=u.id).count()
        plan_name = s.plan.name if s and s.plan else 'Free'
        badge = s.plan.has_verified_badge if s and s.plan else False
        featured = s.plan.is_featured if s and s.plan else False
        all_tutors.append({'user': u, 'profile': p, 'avg_rating': round(avg_rating, 1),
                          'review_count': review_count, 'plan': plan_name,
                          'verified': badge, 'featured': featured})

    return render_template('student/search.html', tutors=all_tutors,
        subject=subject, location=location, max_fee=max_fee, exp_level=exp_level)


@student_bp.route('/teacher/<int:teacher_id>')
@login_required
@student_required
def teacher_profile(teacher_id):
    teacher = User.query.get_or_404(teacher_id)
    if teacher.role != 'teacher':
        flash('Teacher not found.', 'error')
        return redirect(url_for('student.search'))
    profile = TeacherProfile.query.filter_by(user_id=teacher_id).first()
    reviews = Review.query.filter_by(teacher_id=teacher_id).order_by(Review.created_at.desc()).all()
    sub = UserSubscription.query.filter_by(user_id=teacher_id, is_active=True).first()
    plan_name = sub.plan.name if sub and sub.plan else 'Free'
    has_badge = sub.plan.has_verified_badge if sub and sub.plan else False
    avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=teacher_id).scalar() or 0
    review_count = Review.query.filter_by(teacher_id=teacher_id).count()
    is_saved = SavedTutor.query.filter_by(student_id=current_user.id, teacher_id=teacher_id).first() is not None
    is_premium = sub and sub.plan and sub.plan.name == 'Premium'
    return render_template('student/teacher_profile.html',
        teacher=teacher, profile=profile, reviews=reviews,
        avg_rating=round(avg_rating, 1), review_count=review_count,
        plan_name=plan_name, has_badge=has_badge, is_saved=is_saved,
        is_premium=is_premium)


@student_bp.route('/teacher/<int:teacher_id>/save', methods=['POST'])
@login_required
@student_required
def save_tutor(teacher_id):
    existing = SavedTutor.query.filter_by(student_id=current_user.id, teacher_id=teacher_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'saved': False})
    saved = SavedTutor(student_id=current_user.id, teacher_id=teacher_id)
    db.session.add(saved)
    db.session.commit()
    return jsonify({'saved': True})


@student_bp.route('/review/<int:teacher_id>', methods=['POST'])
@login_required
@student_required
def add_review(teacher_id):
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    if not rating or rating < 1 or rating > 5:
        flash('Invalid rating.', 'error')
        return redirect(url_for('student.teacher_profile', teacher_id=teacher_id))
    review = Review(student_id=current_user.id, teacher_id=teacher_id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()
    flash('Review submitted!', 'success')
    return redirect(url_for('student.teacher_profile', teacher_id=teacher_id))


@student_bp.route('/posts')
@login_required
@student_required
def posts():
    all_posts = TuitionPost.query.filter_by(student_id=current_user.id).order_by(TuitionPost.created_at.desc()).all()
    return render_template('student/posts.html', posts=all_posts)


@student_bp.route('/posts/create', methods=['GET', 'POST'])
@login_required
@student_required
def create_post():
    if request.method == 'POST':
        post = TuitionPost(
            student_id=current_user.id,
            title=request.form.get('title'),
            subject=request.form.get('subject'),
            class_level=request.form.get('class_level'),
            location=request.form.get('location'),
            salary=int(request.form.get('salary', 0) or 0),
            description=request.form.get('description'),
            status='Open'
        )
        db.session.add(post)
        db.session.commit()
        flash('Tuition post created!', 'success')
        return redirect(url_for('student.posts'))
    return render_template('student/create_post.html')


@student_bp.route('/post/<int:post_id>/close')
@login_required
@student_required
def close_post(post_id):
    post = TuitionPost.query.get_or_404(post_id)
    if post.student_id != current_user.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('student.posts'))
    post.status = 'Closed'
    db.session.commit()
    flash('Post closed.', 'success')
    return redirect(url_for('student.posts'))


@student_bp.route('/post/<int:post_id>/applications')
@login_required
@student_required
def post_applications(post_id):
    post = TuitionPost.query.get_or_404(post_id)
    if post.student_id != current_user.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('student.posts'))
    apps = Application.query.filter_by(post_id=post_id).order_by(Application.created_at.desc()).all()
    return render_template('student/applications.html', post=post, applications=apps)


@student_bp.route('/application/<int:app_id>/<action>')
@login_required
@student_required
def handle_application(app_id, action):
    app = Application.query.get_or_404(app_id)
    post = TuitionPost.query.get(app.post_id)
    if post.student_id != current_user.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('student.dashboard'))
    if action in ('shortlist', 'select', 'reject'):
        status_map = {'shortlist': 'Shortlisted', 'select': 'Selected', 'reject': 'Rejected'}
        app.status = status_map[action]
        if action == 'select':
            post.status = 'Filled'
        db.session.commit()
        Notification(user_id=app.teacher_id, type='application', title='Application ' + status_map[action],
            message='Your application for "' + post.title + '" has been ' + status_map[action],
            link='/teacher/dashboard')
        db.session.commit()
        flash('Application ' + status_map[action] + '!', 'success')
    return redirect(url_for('student.post_applications', post_id=post.id))


@student_bp.route('/saved-tutors')
@login_required
@student_required
def saved_tutors():
    saved_ids = [s.teacher_id for s in SavedTutor.query.filter_by(student_id=current_user.id).all()]
    tutors = []
    if saved_ids:
        users_map = {u.id: u for u in User.query.filter(User.id.in_(saved_ids)).all()}
        profiles_map = {p.user_id: p for p in TeacherProfile.query.filter(TeacherProfile.user_id.in_(saved_ids)).all()}
        ratings = db.session.query(
            Review.teacher_id, db.func.avg(Review.rating).label('avg'), db.func.count(Review.id).label('cnt')
        ).filter(Review.teacher_id.in_(saved_ids)).group_by(Review.teacher_id).all()
        rating_map = {r.teacher_id: {'avg': round(r.avg, 1), 'cnt': r.cnt} for r in ratings}
        for tid in saved_ids:
            u = users_map.get(tid)
            p = profiles_map.get(tid)
            if u and p:
                r = rating_map.get(tid, {'avg': 0, 'cnt': 0})
                tutors.append({'user': u, 'profile': p, 'avg_rating': r['avg']})
    return render_template('student/saved_tutors.html', tutors=tutors)


@student_bp.route('/messages')
@login_required
@student_required
def messages():
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    received = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).all()
    return render_template('student/messages.html', sent=sent, received=received)


@student_bp.route('/send_message/<int:teacher_id>', methods=['POST'])
@login_required
@student_required
def send_message(teacher_id):
    text = request.form.get('message')
    if not text:
        flash('Message cannot be empty.', 'error')
        return redirect(url_for('student.teacher_profile', teacher_id=teacher_id))
    msg = Message(sender_id=current_user.id, receiver_id=teacher_id, message=text)
    db.session.add(msg)
    db.session.commit()
    Notification(user_id=teacher_id, type='message', title='New Message',
        message='You have a new message from ' + current_user.name, link='/teacher/messages')
    db.session.commit()
    flash('Message sent!', 'success')
    return redirect(url_for('student.teacher_profile', teacher_id=teacher_id))


@student_bp.route('/notifications')
@login_required
@student_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('student/notifications.html', notifications=notifs)


@student_bp.route('/upload-picture', methods=['POST'])
@login_required
@student_required
def upload_picture():
    if 'profile_picture' not in request.files or request.files['profile_picture'].filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('student.edit_profile'))
    url = save_uploaded_file(request.files['profile_picture'], 'profile_pictures', f'student_{current_user.id}')
    if not url:
        flash('Please upload JPG, JPEG, or PNG.', 'error')
        return redirect(url_for('student.edit_profile'))
    current_user.profile_picture = url
    db.session.commit()
    flash('Profile picture updated!', 'success')
    return redirect(url_for('student.edit_profile'))


@student_bp.route('/delete-picture', methods=['POST'])
@login_required
@student_required
def delete_picture():
    current_user.profile_picture = None
    db.session.commit()
    flash('Profile picture removed.', 'success')
    return redirect(url_for('student.edit_profile'))


@student_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@student_required
def edit_profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name)
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('student.dashboard'))
    return render_template('student/edit_profile.html')
