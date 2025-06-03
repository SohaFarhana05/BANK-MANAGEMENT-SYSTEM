from flask_login import LoginManager
from models import BankAdmin

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return BankAdmin.query.get(int(user_id))
