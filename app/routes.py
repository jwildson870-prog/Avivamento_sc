from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from .models import db, SiteContent, Pastor, Notice, Announcement

main = Blueprint('main', __name__)

def content(key, title, body=''):
    item = SiteContent.query.filter_by(key=key).first()
    if not item:
        item = SiteContent(key=key, title=title, body=body)
        db.session.add(item); db.session.commit()
    return item

@main.route('/')
def home():
    church = content('church_bio','Biografia da Igreja','Conte aqui a história, missão, visão e valores da Igreja Avivamento.')
    pastors = Pastor.query.order_by(Pastor.name).all()
    notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()
    return render_template('home.html', church=church, pastors=pastors, notices=notices, announcements=announcements)

@main.route('/pastor/<int:pastor_id>')
def pastor_detail(pastor_id):
    pastor = db.get_or_404(Pastor, pastor_id)
    return render_template('pastor.html', pastor=pastor)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main.route('/avisos')
def notices():
    return render_template('notices.html', notices=Notice.query.order_by(Notice.created_at.desc()).all())

@main.route('/anuncios')
def announcements():
    return render_template('announcements.html', announcements=Announcement.query.order_by(Announcement.created_at.desc()).all())
