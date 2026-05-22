from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Payment, SubscriptionPlan
from datetime import datetime

payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/request/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def request_payment(plan_id):
    plan = SubscriptionPlan.query.get_or_404(plan_id)
    if plan.price == 0:
        flash('This plan is free.', 'info')
        return redirect(url_for('subscriptions.plans'))

    if request.method == 'POST':
        method = request.form.get('method')
        transaction_id = request.form.get('transaction_id')
        sender_number = request.form.get('sender_number')

        errors = []
        if not method: errors.append('Select a payment method.')
        if not transaction_id: errors.append('Transaction ID is required.')
        if not sender_number: errors.append('Sender number is required.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('payments/request.html', plan=plan)

        existing = Payment.query.filter_by(transaction_id=transaction_id).first()
        if existing:
            flash('This transaction ID has already been used.', 'error')
            return render_template('payments/request.html', plan=plan)

        payment = Payment(
            user_id=current_user.id,
            plan_id=plan.id,
            amount=plan.price,
            method=method,
            sender_number=sender_number,
            transaction_id=transaction_id,
            status='Pending'
        )
        db.session.add(payment)
        db.session.commit()

        flash('Payment submitted! Admin will verify and activate your subscription within 24 hours.', 'success')
        return redirect(url_for('teacher.dashboard'))

    return render_template('payments/request.html', plan=plan)


@payments_bp.route('/history')
@login_required
def history():
    payments = Payment.query.filter_by(user_id=current_user.id).order_by(Payment.created_at.desc()).all()
    return render_template('payments/history.html', payments=payments)
