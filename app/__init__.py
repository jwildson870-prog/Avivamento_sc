from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from .models import db, User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Faça login para acessar esta área.'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    from .auth import auth
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            User.create_admin('admin', 'admin@avivamento.local', 'admin123')

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
