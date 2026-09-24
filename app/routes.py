from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from .models import SiteContent, Pastor

main = Blueprint('main', __name__)

def content(key, title, body=''):
    item = SiteContent.query.filter_by(key=key).first()
    if not item:
        item = SiteContent(key=key, title=title, body=body)
        from .models import db
        db.session.add(item); db.session.commit()
    return item

@main.route('/')
def home():
    church = content('church_bio','Biografia da Igreja','Conte aqui a história, missão, visão e valores da Igreja Avivamento.')
    pastors = Pastor.query.order_by(Pastor.name).all()
    return render_template('home.html', church=church, pastors=pastors)

@main.route('/pastor/<int:pastor_id>')
def pastor_detail(pastor_id):
    pastor = Pastor.query.get_or_404(pastor_id)
    return render_template('pastor.html', pastor=pastor)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
