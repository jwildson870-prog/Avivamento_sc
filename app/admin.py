from functools import wraps
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from .models import db, User, Pastor, SiteContent, Notice, Announcement
from .storage import delete_image, save_image, save_media

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
        pastor = Pastor(name=request.form.get('name','').strip(), role=request.form.get('role','Pastor').strip(), bio=request.form.get('bio','').strip())
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


@admin.route('/notices')
@admin_required
def notices():
    return render_template('admin/notices.html', notices=Notice.query.order_by(Notice.created_at.desc()).all())

@admin.route('/notices/new', methods=['POST'])
@admin_required
def new_notice():
    title = request.form.get('title','').strip()
    if not title:
        flash('Informe o título do aviso.', 'error')
        return redirect(url_for('admin.notices'))
    item = Notice(title=title, body=request.form.get('body','').strip())
    file = request.files.get('image')
    if file and file.filename:
        key = save_image(file, 'notice')
        if not key:
            flash('Use JPG, PNG ou WEBP.', 'error')
            return redirect(url_for('admin.notices'))
        item.image = key
    db.session.add(item); db.session.commit()
    flash('Aviso adicionado.', 'success')
    return redirect(url_for('admin.notices'))

@admin.route('/notices/<int:notice_id>/delete', methods=['POST'])
@admin_required
def delete_notice(notice_id):
    item = Notice.query.get_or_404(notice_id)
    delete_image(item.image)
    db.session.delete(item); db.session.commit()
    flash('Aviso removido.', 'success')
    return redirect(url_for('admin.notices'))

@admin.route('/announcements')
@admin_required
def announcements():
    return render_template('admin/announcements.html', announcements=Announcement.query.order_by(Announcement.created_at.desc()).all())

@admin.route('/announcements/new', methods=['POST'])
@admin_required
def new_announcement():
    title = request.form.get('title','').strip()
    if not title:
        flash('Informe o título do anúncio.', 'error')
        return redirect(url_for('admin.announcements'))
    item = Announcement(title=title, body=request.form.get('body','').strip())
    file = request.files.get('media')
    if file and file.filename:
        key = save_media(file, 'announcement', allow_video=True)
        if not key:
            flash('Use JPG, PNG, WEBP, MP4, WEBM ou OGG.', 'error')
            return redirect(url_for('admin.announcements'))
        item.media = key
        item.media_type = 'video' if Path(file.filename).suffix.lower() in {'.mp4','.webm','.ogg'} else 'image'
    db.session.add(item); db.session.commit()
    flash('Anúncio adicionado.', 'success')
    return redirect(url_for('admin.announcements'))

@admin.route('/announcements/<int:announcement_id>/delete', methods=['POST'])
@admin_required
def delete_announcement(announcement_id):
    item = Announcement.query.get_or_404(announcement_id)
    delete_image(item.media)
    db.session.delete(item); db.session.commit()
    flash('Anúncio removido.', 'success')
    return redirect(url_for('admin.announcements'))
