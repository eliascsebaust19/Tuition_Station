from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Message, Notification
from datetime import datetime

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
@login_required
def index():
    conversations = {}
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    received = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).all()

    for m in sent:
        other_id = m.receiver_id
        if other_id not in conversations or conversations[other_id]['last_msg'] < m.created_at:
            other = User.query.get(other_id)
            unread = Message.query.filter_by(sender_id=other_id, receiver_id=current_user.id, is_read=False).count()
            conversations[other_id] = {
                'user': other, 'last_msg': m.created_at, 'last_text': m.message[:50],
                'unread': unread, 'is_sender': True
            }

    for m in received:
        other_id = m.sender_id
        if other_id not in conversations or conversations[other_id]['last_msg'] < m.created_at:
            other = User.query.get(other_id)
            unread = Message.query.filter_by(sender_id=other_id, receiver_id=current_user.id, is_read=False).count()
            conversations[other_id] = {
                'user': other, 'last_msg': m.created_at, 'last_text': m.message[:50],
                'unread': unread, 'is_sender': False
            }
        else:
            conversations[other_id]['unread'] = Message.query.filter_by(
                sender_id=other_id, receiver_id=current_user.id, is_read=False).count()

    sorted_conv = sorted(conversations.values(), key=lambda c: c['last_msg'], reverse=True)
    return render_template('chat/index.html', conversations=sorted_conv)


@chat_bp.route('/<int:user_id>')
@login_required
def conversation(user_id):
    other = User.query.get_or_404(user_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()

    unread = Message.query.filter_by(sender_id=user_id, receiver_id=current_user.id, is_read=False)
    unread.update({'is_read': True, 'read_at': datetime.utcnow()})
    db.session.commit()

    return render_template('chat/conversation.html', other=other, messages=messages)


@chat_bp.route('/send', methods=['POST'])
@login_required
def send():
    receiver_id = request.form.get('receiver_id', type=int)
    text = request.form.get('message', '').strip()

    if not receiver_id or not text:
        flash('Message cannot be empty.', 'error')
        return redirect(request.referrer or url_for('chat.index'))

    receiver = User.query.get(receiver_id)
    if not receiver:
        flash('User not found.', 'error')
        return redirect(url_for('chat.index'))

    msg = Message(sender_id=current_user.id, receiver_id=receiver_id, message=text)
    db.session.add(msg)

    Notification(user_id=receiver_id, type='message', title='New Message',
        message='New message from ' + current_user.name,
        link='/chat/' + str(current_user.id))
    db.session.commit()

    flash('Message sent!', 'success')
    return redirect(url_for('chat.conversation', user_id=receiver_id))


@chat_bp.route('/api/unread')
@login_required
def api_unread():
    count = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    notif_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'messages': count, 'notifications': notif_count, 'total': count + notif_count})
