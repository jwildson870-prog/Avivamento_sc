from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from .models import SiteContent, Pastor, Notice, ScheduleItem, Announcement

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
    return render_template('home.html', church=church, pastors=pastors, notices=Notice.query.filter_by(published=True).order_by(Notice.created_at.desc()).limit(5).all(), announcements=Announcement.query.filter_by(published=True).order_by(Announcement.created_at.desc()).limit(6).all())

@main.route('/pastor/<int:pastor_id>')
def pastor_detail(pastor_id):
    pastor = Pastor.query.get_or_404(pastor_id)
    return render_template('pastor.html', pastor=pastor)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main.route('/igreja')
def church_page():
    church = content('church_bio','Biografia da Igreja','Conte aqui a história, missão, visão e valores da Igreja Avivamento.')
    return render_template('church.html', church=church)

@main.route('/avisos')
def notices_page():
    return render_template('notices.html', notices=Notice.query.filter_by(published=True).order_by(Notice.created_at.desc()).all())

@main.route('/cronograma')
def schedule_page():
    return render_template('schedule.html', items=ScheduleItem.query.filter_by(published=True).order_by(ScheduleItem.day, ScheduleItem.time).all())

@main.route('/pastores')
def pastors_page():
    return render_template('pastors.html', pastors=Pastor.query.order_by(Pastor.name).all())

@main.route('/anuncios')
def announcements_page():
    return render_template('announcements.html', announcements=Announcement.query.filter_by(published=True).order_by(Announcement.created_at.desc()).all())
