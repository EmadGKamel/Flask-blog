from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY_HERE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.domain.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'Host@domain.com'
app.config['MAIL_PASSWORD'] = 'SECRET_PASSWORD'
mail = Mail(app)
db = SQLAlchemy(app)
crypto = Bcrypt(app)
manager = LoginManager(app)
manager.login_view = 'login'
manager.login_message_category = 'info'


from blog import routes
