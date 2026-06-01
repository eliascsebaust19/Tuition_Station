from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from models import db, User, TeacherProfile, SubscriptionPlan, UserSubscription, Payment, TuitionPost, Application, Message, Notification, Review, ToDo
from datetime import datetime, timedelta
from routes.utils import role_required, save_uploaded_file

teacher_bp = Blueprint('teacher', __name__)
teacher_required = role_required('teacher')


@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    profile = TeacherProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = TeacherProfile(user_id=current_user.id, subject='', fee=0)
        db.session.add(profile)
        db.session.commit()

    sub = UserSubscription.query.filter_by(user_id=current_user.id, is_active=True).first()
    plan = sub.plan if sub else SubscriptionPlan.query.filter_by(name='Free').first()
    days_left = sub.days_remaining if sub else 0

    applications = Application.query.filter_by(teacher_id=current_user.id).order_by(Application.created_at.desc()).all()
    pending_apps = Application.query.filter_by(teacher_id=current_user.id, status='Pending').count()
    selected_apps = Application.query.filter_by(teacher_id=current_user.id, status='Selected').count()
    reviews = Review.query.filter_by(teacher_id=current_user.id).order_by(Review.created_at.desc()).all()
    avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=current_user.id).scalar() or 0
    unread_messages = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    todos = ToDo.query.filter_by(user_id=current_user.id, is_completed=False).all()

    open_posts = TuitionPost.query.filter_by(status='Open').count()
    total_posts = TuitionPost.query.count()

    return render_template('teacher/dashboard.html',
        profile=profile, plan=plan, sub=sub, days_left=days_left,
        applications=applications, pending_apps=pending_apps, selected_apps=selected_apps,
        reviews=reviews, avg_rating=round(avg_rating, 1), review_count=len(reviews),
        unread_messages=unread_messages, notifications=notifications,
        todos=todos, open_posts=open_posts, total_posts=total_posts)


@teacher_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@teacher_required
def profile():
    profile = TeacherProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = TeacherProfile(user_id=current_user.id, subject='', fee=0)
        db.session.add(profile)
        db.session.commit()

    if request.method == 'POST':
        text_fields = ['university', 'department', 'degree', 'subject', 'location', 'bio', 'availability',
                       'qualification', 'subjects_expert_in', 'class_level', 'teaching_areas',
                       'languages', 'teaching_style', 'availability_schedule', 'social_links',
                       'intro_video_url', 'notes_resources', 'key_strengths', 'why_students_notice',
                       'tuition_experience', 'reasons_to_hire', 'preface']
        for field in text_fields:
            val = request.form.get(field)
            if val is not None:
                setattr(profile, field, val)
        profile.graduation_year = request.form.get('graduation_year', type=int) or profile.graduation_year
        profile.experience = request.form.get('experience', type=int) or profile.experience
        profile.fee = request.form.get('fee', type=int) or profile.fee
        profile.hourly_fee = request.form.get('hourly_fee', type=int)
        profile.total_students_taught = request.form.get('total_students_taught', type=int) or profile.total_students_taught
        profile.success_percentage = request.form.get('success_percentage', type=int)
        profile.teaching_mode = request.form.get('teaching_mode', 'both')
        profile.demo_class_available = request.form.get('demo_class_available') == 'on'

        required = ['university', 'department', 'graduation_year', 'subject', 'fee', 'location']
        profile.is_complete = all(getattr(profile, f) for f in required) and profile.cv is not None
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('teacher.profile'))

    sub = UserSubscription.query.filter_by(user_id=current_user.id, is_active=True).first()
    plan = sub.plan if sub else SubscriptionPlan.query.filter_by(name='Free').first()
    days_left = sub.days_remaining if sub else 0
    return render_template('teacher/profile.html', profile=profile, plan=plan, days_left=days_left)


@teacher_bp.route('/upload-picture', methods=['POST'])
@login_required
@teacher_required
def upload_picture():
    if 'profile_picture' not in request.files or request.files['profile_picture'].filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('teacher.profile'))
    url = save_uploaded_file(request.files['profile_picture'], 'profile_pictures', f'teacher_{current_user.id}')
    if not url:
        flash('Please upload JPG, JPEG, or PNG.', 'error')
        return redirect(url_for('teacher.profile'))
    current_user.profile_picture = url
    db.session.commit()
    flash('Profile picture updated!', 'success')
    return redirect(url_for('teacher.profile'))


@teacher_bp.route('/upload-cv', methods=['POST'])
@login_required
@teacher_required
def upload_cv():
    if 'cv' not in request.files or request.files['cv'].filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('teacher.profile'))
    url = save_uploaded_file(request.files['cv'], 'cvs', f'cv_{current_user.id}', {'pdf', 'doc', 'docx'})
    if not url:
        flash('Please upload PDF, DOC, or DOCX.', 'error')
        return redirect(url_for('teacher.profile'))
    profile = TeacherProfile.query.filter_by(user_id=current_user.id).first()
    if profile:
        profile.cv = url
        db.session.commit()
    flash('CV uploaded!', 'success')
    return redirect(url_for('teacher.profile'))


@teacher_bp.route('/browse-posts')
@login_required
@teacher_required
def browse_posts():
    subject = request.args.get('subject', '')
    location = request.args.get('location', '')
    query = TuitionPost.query.filter_by(status='Open')
    if subject:
        query = query.filter(TuitionPost.subject.ilike(f'%{subject}%'))
    if location:
        query = query.filter(TuitionPost.location.ilike(f'%{location}%'))
    posts = query.order_by(TuitionPost.created_at.desc()).all()

    sub = UserSubscription.query.filter_by(user_id=current_user.id, is_active=True).first()
    plan = sub.plan if sub else SubscriptionPlan.query.filter_by(name='Free').first()

    post_data = []
    for p in posts:
        already_applied = Application.query.filter_by(post_id=p.id, teacher_id=current_user.id).first() is not None
        post_data.append({'post': p, 'already_applied': already_applied})

    return render_template('teacher/browse_posts.html', posts=post_data, plan=plan, subject=subject, location=location)


@teacher_bp.route('/apply/<int:post_id>', methods=['POST'])
@login_required
@teacher_required
def apply_post(post_id):
    post = TuitionPost.query.get_or_404(post_id)
    if post.status != 'Open':
        flash('This post is no longer open.', 'error')
        return redirect(url_for('teacher.browse_posts'))

    existing = Application.query.filter_by(post_id=post_id, teacher_id=current_user.id).first()
    if existing:
        flash('You already applied to this post.', 'warning')
        return redirect(url_for('teacher.browse_posts'))

    sub = UserSubscription.query.filter_by(user_id=current_user.id, is_active=True).first()
    plan = sub.plan if sub else SubscriptionPlan.query.filter_by(name='Free').first()

    if plan.max_applications is not None:
        monthly_count = Application.query.filter(
            Application.teacher_id == current_user.id,
            Application.created_at >= datetime.utcnow().replace(day=1)
        ).count()
        if monthly_count >= plan.max_applications:
            flash('You have reached your monthly application limit (' + str(plan.max_applications) + '). Upgrade to apply more.', 'error')
            return redirect(url_for('subscriptions.plans'))

    message = request.form.get('message', '')
    app = Application(post_id=post_id, teacher_id=current_user.id, message=message, status='Pending')
    db.session.add(app)
    db.session.commit()

    Notification(user_id=post.student_id, type='application', title='New Application',
        message=current_user.name + ' applied to your post: ' + post.title,
        link='/student/post/' + str(post_id) + '/applications')
    db.session.commit()

    flash('Application submitted!', 'success')
    return redirect(url_for('teacher.browse_posts'))


@teacher_bp.route('/analytics')
@login_required
@teacher_required
def analytics():
    monthly_apps = db.session.query(
        db.func.year(Application.created_at).label('year'),
        db.func.month(Application.created_at).label('month'),
        db.func.count(Application.id).label('count')
    ).filter(Application.teacher_id == current_user.id).group_by(
        db.func.year(Application.created_at), db.func.month(Application.created_at)
    ).order_by(db.desc('year'), db.desc('month')).limit(6).all()

    status_counts = db.session.query(
        Application.status, db.func.count(Application.id).label('count')
    ).filter(Application.teacher_id == current_user.id).group_by(Application.status).all()

    return render_template('teacher/analytics.html', monthly_apps=monthly_apps, status_counts=status_counts)


@teacher_bp.route('/messages')
@login_required
@teacher_required
def messages():
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    received = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).all()

    Message.query.filter_by(receiver_id=current_user.id, is_read=False).update({'is_read': True, 'read_at': datetime.utcnow()})
    db.session.commit()
    return render_template('teacher/messages.html', sent=sent, received=received)


@teacher_bp.route('/reply_message/<int:student_id>', methods=['POST'])
@login_required
@teacher_required
def reply_message(student_id):
    text = request.form.get('message')
    if not text:
        flash('Message cannot be empty.', 'error')
        return redirect(url_for('teacher.messages'))
    msg = Message(sender_id=current_user.id, receiver_id=student_id, message=text)
    db.session.add(msg)
    db.session.commit()
    flash('Message sent!', 'success')
    return redirect(url_for('teacher.messages'))


@teacher_bp.route('/notifications')
@login_required
@teacher_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('teacher/notifications.html', notifications=notifs)


@teacher_bp.route('/payment-history')
@login_required
@teacher_required
def payment_history():
    payments = Payment.query.filter_by(user_id=current_user.id).order_by(Payment.created_at.desc()).all()
    return render_template('teacher/payment_history.html', payments=payments)


@teacher_bp.route('/api/stats')
@login_required
@teacher_required
def api_stats():
    pending = Application.query.filter_by(teacher_id=current_user.id, status='Pending').count()
    selected = Application.query.filter_by(teacher_id=current_user.id, status='Selected').count()
    total = Application.query.filter_by(teacher_id=current_user.id).count()
    reviews = Review.query.filter_by(teacher_id=current_user.id).count()
    avg = db.session.query(db.func.avg(Review.rating)).filter_by(teacher_id=current_user.id).scalar() or 0
    return jsonify({
        'pending_applications': pending, 'selected_applications': selected,
        'total_applications': total, 'total_reviews': reviews, 'avg_rating': round(float(avg), 1)
    })
