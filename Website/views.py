from cmath import log
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Gift, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        gift_title = request.form.get('title')
        gift_price = request.form.get('price')
        gift_description = request.form.get('description')
        gift_link = request.form.get('link_to')
        if(gift_link == ''):
            gift_link = 'https://google.com/search?q=' + gift_title
        new_gift = Gift(title=gift_title, description=gift_description, price=gift_price, link=gift_link, gift_user_id=current_user.id)
        db.session.add(new_gift)
        db.session.commit()
        flash('Gift added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-gift', methods=['POST'])
@login_required
def delete_gift():
    gift = json.loads(request.data)
    giftID = gift['giftID']
    gift = Gift.query.get(giftID)
    if gift:
        if gift.gift_user_id == current_user.id:
            db.session.delete(gift)
            db.session.commit()
            flash('Gift removed!', category='error')

        
    return jsonify({})
