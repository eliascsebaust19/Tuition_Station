from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, TeacherProfile, SubscriptionPlan, UserSubscription, Payment, TuitionPost, Application, Message, Notification, Review, ToDo, AdminLog
from datetime import datetime
from routes.utils import role_required

admin_bp = Blueprint('admin', __name__)
admin_required = role_required('admin')


def log(action, entity_type=None, entity_id=None, details=None):
    log = AdminLog(admin_id=current_user.id, action=action,
                   entity_type=entity_type, entity_id=entity_id, details=details)
    db.session.add(log)
    db.session.commit()


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_teachers = User.query.filter_by(role='teacher').count()
    pending_teachers = User.query.filter_by(role='teacher', is_approved=False).count()
    pending_payments = Payment.query.filter_by(status='Pending').count()
    open_posts = TuitionPost.query.filter_by(status='Open').count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status='Approved').scalar() or 0
    unread_messages = Message.query.filter_by(is_read=False).count()
    total_requests = Application.query.count()
    pending_messages = Message.query.filter_by(is_read=False).count()

    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    logs = AdminLog.query.order_by(AdminLog.created_at.desc()).limit(10).all()
    all_users = User.query.order_by(User.created_at.desc()).all()
    all_requests = Application.query.join(TuitionPost, Application.post_id == TuitionPost.id).order_by(Application.created_at.desc()).all()

    return render_template('admin/dashboard.html',
        total_students=total_students, total_teachers=total_teachers,
        pending_teachers=pending_teachers, pending_payments=pending_payments,
        open_posts=open_posts, total_revenue=total_revenue,
        unread_messages=unread_messages, recent_payments=recent_payments,
        recent_users=recent_users, logs=logs, total_requests=total_requests,
        pending_messages=pending_messages, all_users=all_users, all_requests=all_requests)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    role_filter = request.args.get('role')
    query = User.query
    if role_filter:
        query = query.filter_by(role=role_filter)
    users = query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/user/<int:user_id>/toggle')
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'blocked'
    log('User ' + status, 'user', user_id, user.name + ' ' + status)
    flash('User ' + status + ' successfully!', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/user/<int:user_id>/delete')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot delete admin users.', 'error')
        return redirect(url_for('admin.users'))
    name = user.name
    db.session.delete(user)
    db.session.commit()
    log('User deleted', 'user', user_id, name + ' deleted')
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/teacher/<int:user_id>/approve')
@login_required
@admin_required
def approve_teacher(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'teacher':
        flash('User is not a teacher.', 'error')
        return redirect(url_for('admin.users'))
    user.is_approved = True
    db.session.commit()
    log('Teacher approved', 'teacher', user_id, user.name + ' approved')
    db.session.add(Notification(user_id=user_id, type='account', title='Account Approved',
        message='Your teacher account has been approved! You can now apply for tuition jobs.', link='/teacher/dashboard'))
    db.session.commit()
    flash('Teacher approved successfully!', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/payments')
@login_required
@admin_required
def payments():
    status_filter = request.args.get('status')
    query = Payment.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    all_payments = query.order_by(Payment.created_at.desc()).all()
    return render_template('admin/payments.html', payments=all_payments)


@admin_bp.route('/payment/<int:payment_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    action = request.form.get('action')
    note = request.form.get('admin_note', '')

    if action == 'approve':
        payment.status = 'Approved'
        payment.verified_by = current_user.id
        payment.verified_at = datetime.utcnow()
        payment.admin_note = note

        plan = SubscriptionPlan.query.get(payment.plan_id)
        if plan:
            UserSubscription.query.filter_by(user_id=payment.user_id, is_active=True).update({'is_active': False})
            sub = UserSubscription(
                user_id=payment.user_id, plan_id=plan.id,
                start_date=datetime.utcnow(), end_date=datetime.utcnow(),
                is_active=True
            )
            from datetime import timedelta
            sub.end_date = sub.start_date + timedelta(days=plan.duration_days)
            db.session.add(sub)
        db.session.add(Notification(user_id=payment.user_id, type='payment', title='Payment Approved',
            message='Your payment of BDT ' + str(payment.amount) + ' has been approved. ' + plan.name + ' plan is now active!',
            link='/teacher/dashboard'))
        db.session.commit()
        log('Payment approved', 'payment', payment_id, 'BDT ' + str(payment.amount))
        flash('Payment approved and subscription activated!', 'success')

    elif action == 'reject':
        payment.status = 'Rejected'
        payment.verified_by = current_user.id
        payment.verified_at = datetime.utcnow()
        payment.admin_note = note
        db.session.add(Notification(user_id=payment.user_id, type='payment', title='Payment Rejected',
            message='Your payment of BDT ' + str(payment.amount) + ' was rejected. Reason: ' + (note or 'No reason provided.'),
            link='/payments/history'))
        db.session.commit()
        log('Payment rejected', 'payment', payment_id, 'BDT ' + str(payment.amount) + ' - ' + note)
        flash('Payment rejected.', 'success')

    return redirect(url_for('admin.payments'))


@admin_bp.route('/requests')
@login_required
@admin_required
def requests():
    all_requests = Application.query.join(TuitionPost, Application.post_id == TuitionPost.id).join(
        User, TuitionPost.student_id == User.id
    ).order_by(Application.created_at.desc()).all()
    return render_template('admin/requests.html', requests=all_requests)


@admin_bp.route('/posts')
@login_required
@admin_required
def posts():
    all_posts = TuitionPost.query.order_by(TuitionPost.created_at.desc()).all()
    return render_template('admin/posts.html', posts=all_posts)


@admin_bp.route('/post/<int:post_id>/toggle')
@login_required
@admin_required
def toggle_post(post_id):
    post = TuitionPost.query.get_or_404(post_id)
    post.status = 'Closed' if post.status == 'Open' else 'Open'
    db.session.commit()
    flash('Post status updated!', 'success')
    return redirect(url_for('admin.posts'))


@admin_bp.route('/messages')
@login_required
@admin_required
def messages():
    all_messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin/messages.html', messages=all_messages)


@admin_bp.route('/subscriptions')
@login_required
@admin_required
def subscriptions():
    all_subs = UserSubscription.query.order_by(UserSubscription.created_at.desc()).all()
    return render_template('admin/subscriptions.html', subscriptions=all_subs)


@admin_bp.route('/request/<int:request_id>/approve')
@login_required
@admin_required
def approve_request(request_id):
    req = Application.query.get_or_404(request_id)
    req.status = 'approved'
    db.session.commit()
    if req.teacher:
        db.session.add(Notification(user_id=req.teacher_id, type='application', title='Application Approved',
            message='Your application for post #' + str(req.post_id) + ' has been approved!', link='/teacher/applications'))
    db.session.commit()
    log('Request approved', 'request', request_id, 'Application ' + str(request_id) + ' approved')
    flash('Request approved!', 'success')
    return redirect(url_for('admin.requests'))


@admin_bp.route('/request/<int:request_id>/reject')
@login_required
@admin_required
def reject_request(request_id):
    req = Application.query.get_or_404(request_id)
    req.status = 'rejected'
    db.session.commit()
    log('Request rejected', 'request', request_id, 'Application ' + str(request_id) + ' rejected')
    flash('Request rejected.', 'success')
    return redirect(url_for('admin.requests'))


@admin_bp.route('/upload-picture', methods=['POST'])
@login_required
@admin_required
def upload_picture():
    from routes.utils import save_uploaded_file
    if 'profile_picture' not in request.files or request.files['profile_picture'].filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('admin.dashboard'))
    url = save_uploaded_file(request.files['profile_picture'], 'profile_pictures', f'admin_{current_user.id}')
    if not url:
        flash('Invalid image format.', 'error')
        return redirect(url_for('admin.dashboard'))
    current_user.profile_picture = url
    db.session.commit()
    flash('Profile picture updated!', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/delete-picture', methods=['POST'])
@login_required
@admin_required
def delete_picture():
    current_user.profile_picture = None
    db.session.commit()
    flash('Profile picture removed.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    monthly_revenue = db.session.query(
        db.func.year(Payment.verified_at).label('year'),
        db.func.month(Payment.verified_at).label('month'),
        db.func.count(Payment.id).label('count'),
        db.func.sum(Payment.amount).label('revenue')
    ).filter(Payment.status == 'Approved').group_by(
        db.func.year(Payment.verified_at), db.func.month(Payment.verified_at)
    ).order_by(db.desc(db.func.year(Payment.verified_at)), db.desc(db.func.month(Payment.verified_at))).all()

    plan_stats = db.session.query(
        SubscriptionPlan.name,
        db.func.count(UserSubscription.id).label('subscribers')
    ).join(UserSubscription, UserSubscription.plan_id == SubscriptionPlan.id
    ).filter(UserSubscription.is_active == True).group_by(SubscriptionPlan.name).all()

    return render_template('admin/reports.html', monthly_revenue=monthly_revenue, plan_stats=plan_stats)


@admin_bp.route('/documentation')
@login_required
@admin_required
def documentation():
    return render_template('admin/documentation.html')
