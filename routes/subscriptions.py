from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, SubscriptionPlan, UserSubscription

subscriptions_bp = Blueprint('subscriptions', __name__)


@subscriptions_bp.route('/plans')
def plans():
    all_plans = SubscriptionPlan.query.order_by(SubscriptionPlan.price).all()
    current_sub = None
    if current_user.is_authenticated:
        current_sub = UserSubscription.query.filter_by(user_id=current_user.id, is_active=True).first()
    return render_template('subscriptions/plans.html', plans=all_plans, current_sub=current_sub)


@subscriptions_bp.route('/upgrade/<int:plan_id>', methods=['POST'])
@login_required
def upgrade(plan_id):
    if current_user.role != 'teacher':
        flash('Only teachers can upgrade subscription plans.', 'error')
        return redirect(url_for('auth.index'))

    plan = SubscriptionPlan.query.get_or_404(plan_id)
    if plan.price == 0:
        return redirect(url_for('subscriptions.plans'))

    return redirect(url_for('payments.request_payment', plan_id=plan.id))
