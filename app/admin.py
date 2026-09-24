from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from .models import db, User, Pastor, SiteContent, Notice, ScheduleItem, Announcement
from .storage import delete_image, save_image

admin = Blueprint('admin', __name__)

def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.role != 'admin': abort(403)
        return view(*args, **kwargs)
    return wrapped

@admin.route('/')
@admin_required
def dashboard():
    church = SiteContent.query.filter_by(key='church_bio').first()
    if not church:
        church = SiteContent(key='church_bio', title='Biografia da Igreja', body='')
        db.session.add(church); db.session.commit()
    return render_template('admin/dashboard.html', users=User.query.count(), pastors=Pastor.query.count(), church=church)

@admin.route('/church', methods=['POST'])
@admin_required
def church():
    item = SiteContent.query.filter_by(key='church_bio').first()
    item.title = request.form.get('title','Biografia da Igreja').strip()
    item.body = request.form.get('body','').strip()
    db.session.commit()
    flash('Biografia da igreja atualizada.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/pastors')
@admin_required
def pastors():
    return render_template('admin/pastors.html', pastors=Pastor.query.order_by(Pastor.name).all())

@admin.route('/pastors/new', methods=['GET','POST'])
@admin_required
def new_pastor():
    if request.method == 'POST':
        pastor = Pastor(name=request.form.get('name','').strip(), role=request.form.get('role','Pastor').strip(), bio=request.form.get('bio','').strip(), teaching=request.form.get('teaching','').strip())
        file = request.files.get('photo')
        if file and file.filename:
            new_key = save_image(file, 'pastor')
            if new_key:
                pastor.photo = new_key
            else:
                flash('Use JPG, PNG ou WEBP.', 'error')
        if not pastor.name:
            flash('Informe o nome do pastor.', 'error')
        else:
            db.session.add(pastor); db.session.commit(); flash('Pastor adicionado.', 'success'); return redirect(url_for('admin.pastors'))
    return render_template('admin/pastor_form.html', pastor=None)

@admin.route('/pastors/<int:pastor_id>/edit', methods=['GET','POST'])
@admin_required
def edit_pastor(pastor_id):
    pastor = Pastor.query.get_or_404(pastor_id)
    if request.method == 'POST':
        pastor.name = request.form.get('name','').strip()
        pastor.role = request.form.get('role','Pastor').strip()
        pastor.bio = request.form.get('bio','').strip()
        pastor.teaching = request.form.get('teaching','').strip()
        file = request.files.get('photo')
        if file and file.filename:
            new_key = save_image(file, 'pastor')
            if new_key:
                old = pastor.photo
                pastor.photo = new_key
                delete_image(old)
            else:
                flash('Use JPG, PNG ou WEBP.', 'error')
        db.session.commit(); flash('Pastor atualizado.', 'success'); return redirect(url_for('admin.pastors'))
    return render_template('admin/pastor_form.html', pastor=pastor)

@admin.route('/pastors/<int:pastor_id>/delete', methods=['POST'])
@admin_required
def delete_pastor(pastor_id):
    pastor = Pastor.query.get_or_404(pastor_id)
    delete_image(pastor.photo)
    db.session.delete(pastor); db.session.commit(); flash('Pastor removido.', 'success')
    return redirect(url_for('admin.pastors'))

@admin.route('/users')
@admin_required
def users():
    return render_template('admin/users.html', users=User.query.order_by(User.created_at.desc()).all())


@admin.route('/notices', methods=['GET','POST'])
@admin_required
def notices():
    if request.method == 'POST':
        item = Notice(title=request.form.get('title','').strip(), body=request.form.get('body','').strip(), published=request.form.get('published') == '1')
        if not item.title:
            flash('Informe o título do aviso.', 'error')
        else:
            db.session.add(item); db.session.commit(); flash('Aviso publicado.', 'success')
    return render_template('admin/notices.html', notices=Notice.query.order_by(Notice.created_at.desc()).all())

@admin.route('/notices/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_notice(item_id):
    item = Notice.query.get_or_404(item_id); db.session.delete(item); db.session.commit(); flash('Aviso removido.', 'success'); return redirect(url_for('admin.notices'))

@admin.route('/schedule', methods=['GET','POST'])
@admin_required
def schedule():
    if request.method == 'POST':
        item = ScheduleItem(title=request.form.get('title','').strip(), day=request.form.get('day','').strip(), time=request.form.get('time','').strip(), description=request.form.get('description','').strip(), published=request.form.get('published') == '1')
        if not item.title or not item.day:
            flash('Informe o título e o dia do cronograma.', 'error')
        else:
            db.session.add(item); db.session.commit(); flash('Item adicionado ao cronograma.', 'success')
    return render_template('admin/schedule.html', items=ScheduleItem.query.order_by(ScheduleItem.created_at.desc()).all())

@admin.route('/schedule/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_schedule(item_id):
    item = ScheduleItem.query.get_or_404(item_id); db.session.delete(item); db.session.commit(); flash('Item removido.', 'success'); return redirect(url_for('admin.schedule'))

@admin.route('/announcements', methods=['GET','POST'])
@admin_required
def announcements():
    if request.method == 'POST':
        title=request.form.get('title','').strip(); description=request.form.get('description','').strip()
        media_type=request.form.get('media_type','none')
        item=Announcement(title=title, description=description, media_type=media_type if media_type in {'none','image','video'} else 'none', published=request.form.get('published') == '1')
        file=request.files.get('media')
        if file and file.filename:
            prefix='announcement_video' if item.media_type=='video' else 'announcement'
            key=save_image(file, prefix)
            if not key:
                flash('Use JPG, PNG ou WEBP para imagens e vídeos compatíveis com o armazenamento configurado.', 'error')
            else:
                item.media=key
        if not title:
            flash('Informe o título do anúncio.', 'error')
        else:
            db.session.add(item); db.session.commit(); flash('Anúncio publicado.', 'success')
    return render_template('admin/announcements.html', announcements=Announcement.query.order_by(Announcement.created_at.desc()).all())

@admin.route('/announcements/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_announcement(item_id):
    item=Announcement.query.get_or_404(item_id); delete_image(item.media); db.session.delete(item); db.session.commit(); flash('Anúncio removido.', 'success'); return redirect(url_for('admin.announcements'))
