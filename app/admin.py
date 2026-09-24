from pathlib import Path
from uuid import uuid4
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import db, User, Pastor, SiteContent

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
            ext = Path(secure_filename(file.filename)).suffix.lower()
            if ext in {'.jpg','.jpeg','.png','.webp'}:
                filename = f'pastor_{uuid4().hex}{ext}'
                file.save(Path(current_app.config['UPLOAD_FOLDER']) / filename)
                pastor.photo = filename
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
            ext = Path(secure_filename(file.filename)).suffix.lower()
            if ext in {'.jpg','.jpeg','.png','.webp'}:
                if pastor.photo:
                    old = Path(current_app.config['UPLOAD_FOLDER']) / pastor.photo
                    if old.exists(): old.unlink()
                filename = f'pastor_{uuid4().hex}{ext}'
                file.save(Path(current_app.config['UPLOAD_FOLDER']) / filename)
                pastor.photo = filename
        db.session.commit(); flash('Pastor atualizado.', 'success'); return redirect(url_for('admin.pastors'))
    return render_template('admin/pastor_form.html', pastor=pastor)

@admin.route('/pastors/<int:pastor_id>/delete', methods=['POST'])
@admin_required
def delete_pastor(pastor_id):
    pastor = Pastor.query.get_or_404(pastor_id)
    if pastor.photo:
        p = Path(current_app.config['UPLOAD_FOLDER']) / pastor.photo
        if p.exists(): p.unlink()
    db.session.delete(pastor); db.session.commit(); flash('Pastor removido.', 'success')
    return redirect(url_for('admin.pastors'))

@admin.route('/users')
@admin_required
def users():
    return render_template('admin/users.html', users=User.query.order_by(User.created_at.desc()).all())
