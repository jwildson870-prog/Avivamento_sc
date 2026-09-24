from pathlib import Path
from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, CSRFError
from .models import db, User
from .migrations import run_migrations
from .storage import image_url

login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Faça login para acessar esta área.'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    app.jinja_env.globals['image_url'] = image_url
    login_manager.init_app(app)
    csrf.init_app(app)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        app.logger.warning('Requisição bloqueada por CSRF: %s', error.description)
        return render_template('errors/400.html', message='A solicitação expirou ou não é válida. Recarregue a página e tente novamente.'), 400

    from .routes import main
    from .auth import auth
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    with app.app_context():
        run_migrations()
        if app.config.get('INITIAL_ADMIN_PASSWORD') and not User.query.filter_by(username=app.config['INITIAL_ADMIN_USERNAME']).first():
            User.create_admin(app.config['INITIAL_ADMIN_USERNAME'], app.config['INITIAL_ADMIN_EMAIL'], app.config['INITIAL_ADMIN_PASSWORD'])

    return app

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
