
# Dont' use Formatter on this file!
# Will shift "from stamp_manager import routes" to front and make circular imports


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e86448051b5cedf049dec758cc706ae4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


# here to avoid circular imports
from stamp_manager import routes