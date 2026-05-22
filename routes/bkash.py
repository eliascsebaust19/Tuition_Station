from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Payment, SubscriptionPlan, UserSubscription, Notification
from bkash_config import BkashConfig, BkashAPI
from datetime import datetime, timedelta

bkash_bp = Blueprint('bkash', __name__, url_prefix='/bkash')


@bkash_bp.route('/create-payment', methods=['POST'])
@login_required
def create_payment():
    plan_id = request.form.get('plan_id')
    if not plan_id:
        return jsonify({'success': False, 'error': 'Plan ID required'}), 400

    plan = SubscriptionPlan.query.get(plan_id)
    if not plan or plan.price == 0:
        return jsonify({'success': False, 'error': 'Invalid plan'}), 400

    invoice = f'TXN-{current_user.id}-{int(datetime.utcnow().timestamp())}'

    if not BkashConfig.is_configured():
        payment = Payment(
            user_id=current_user.id, plan_id=plan.id, amount=plan.price,
            method='bKash', sender_number='',
            transaction_id=invoice, status='Pending'
        )
        db.session.add(payment)
        db.session.commit()
        return jsonify({
            'success': True,
            'demo': True,
            'redirect': url_for('bkash.payment_success', payment_id=payment.id)
        })

    try:
        cb_url = url_for('bkash.callback', _external=True)
        result = BkashAPI.create_payment(
            amount=plan.price,
            invoice_number=invoice,
            payer_reference=str(current_user.id),
            callback_url=cb_url
        )

        payment = Payment(
            user_id=current_user.id, plan_id=plan.id, amount=plan.price,
            method='bKash', sender_number='',
            transaction_id=invoice, status='Pending'
        )
        db.session.add(payment)
        db.session.commit()

        return jsonify({
            'success': True,
            'paymentID': result.get('paymentID'),
            'bkashURL': result.get('bkashURL'),
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bkash_bp.route('/callback')
def callback():
    payment_id = request.args.get('paymentID')
    status = request.args.get('status')
    error = request.args.get('error', '')

    if status == 'cancel':
        flash('Payment cancelled.', 'warning')
        return redirect(url_for('subscriptions.plans'))

    if not payment_id:
        flash('Invalid payment response.', 'error')
        return redirect(url_for('subscriptions.plans'))

    if not BkashConfig.is_configured():
        return redirect(url_for('bkash.payment_success', payment_id=0))

    try:
        result = BkashAPI.execute_payment(payment_id)
        trx_id = result.get('trxID', payment_id)

        payment = Payment.query.filter_by(transaction_id=result.get('merchantInvoiceNumber', '')).first()
        if payment:
            payment.transaction_id = trx_id
            payment.status = 'Approved'
            payment.sender_number = result.get('customerMsisdn', '')
            payment.verified_at = datetime.utcnow()
            db.session.commit()

            sub = UserSubscription.query.filter_by(user_id=payment.user_id, is_active=True).first()
            if sub:
                sub.is_active = False
            new_sub = UserSubscription(
                user_id=payment.user_id, plan_id=payment.plan_id,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=payment.plan_ref.duration_days or 30),
                is_active=True
            )
            db.session.add(new_sub)
            notif = Notification(user_id=payment.user_id, type='payment', title='Payment Approved',
                message='Your bKash payment of BDT ' + str(payment.amount) + ' has been approved. ' + (payment.plan_ref.name if payment.plan_ref else '') + ' plan is now active!',
                link='/teacher/dashboard')
            db.session.add(notif)
            db.session.commit()

        flash('Payment successful! Your subscription is now active.', 'success')
        return redirect(url_for('teacher.dashboard'))
    except Exception as e:
        flash(f'Payment verification failed: {str(e)}', 'error')
        return redirect(url_for('subscriptions.plans'))


@bkash_bp.route('/payment-success/<int:payment_id>')
@login_required
def payment_success(payment_id):
    if payment_id > 0:
        payment = Payment.query.get(payment_id)
        if payment and payment.user_id == current_user.id and payment.status == 'Pending':
            payment.status = 'Approved'
            payment.verified_at = datetime.utcnow()
            db.session.commit()

            sub = UserSubscription.query.filter_by(user_id=current_user.id, is_active=True).first()
            if sub:
                sub.is_active = False
            new_sub = UserSubscription(
                user_id=current_user.id, plan_id=payment.plan_id,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=payment.plan_ref.duration_days or 30),
                is_active=True
            )
            db.session.add(new_sub)
            notif = Notification(user_id=current_user.id, type='payment', title='Payment Approved',
                message='Your bKash payment of BDT ' + str(payment.amount) + ' has been approved. ' + (payment.plan_ref.name if payment.plan_ref else '') + ' plan is now active!',
                link='/teacher/dashboard')
            db.session.add(notif)
            db.session.commit()

    flash('Payment successful! Your subscription is now active.', 'success')
    return redirect(url_for('teacher.dashboard'))
