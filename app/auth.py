from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User
from .storage import delete_image, save_image

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        identity = request.form.get('identity','').strip()
        password = request.form.get('password','')
        user = User.query.filter((User.username == identity) | (User.email == identity)).first()
        if user and user.check_password(password):
            login_user(user, remember=request.form.get('remember') == '1')
            return redirect(url_for('main.home'))
        flash('Usuário/e-mail ou senha inválidos.', 'error')
    return render_template('login.html')

@auth.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        email = request.form.get('email','').strip().lower()
        password = request.form.get('password','')
        if len(username) < 3 or len(password) < 6:
            flash('Usuário deve ter 3+ caracteres e a senha 6+.', 'error')
        elif User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Usuário ou e-mail já cadastrado.', 'error')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user); db.session.commit()
            login_user(user)
            flash('Conta criada com sucesso.', 'success')
            return redirect(url_for('main.profile'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da conta.', 'success')
    return redirect(url_for('main.home'))

@auth.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    if current_user.role == 'admin':
        flash('A conta principal de administrador não pode ser apagada por esta tela.', 'error')
        return redirect(url_for('main.profile'))
    user = current_user
    photo = user.photo
    db.session.delete(user); db.session.commit()
    delete_image(photo)
    logout_user()
    flash('Sua conta foi excluída.', 'success')
    return redirect(url_for('main.home'))

@auth.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':
        file = request.files.get('photo')
        if file and file.filename:
            new_key = save_image(file, f'user_{current_user.id}')
            if not new_key:
                flash('Use JPG, PNG ou WEBP.', 'error')
            else:
                old = current_user.photo
                current_user.photo = new_key
                db.session.commit()
                delete_image(old)
                flash('Foto atualizada.', 'success')
        return redirect(url_for('main.profile'))
    return render_template('profile.html')
