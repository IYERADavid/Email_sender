import os
from flask import Flask
from app.view import web
from datetime import timedelta
from flaskext.autoversion import Autoversion

app = Flask(__name__)
# TODO add a function to retrieve environment variables
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.autoversion = True
Autoversion(app)
app.permanent_session_lifetime = timedelta(days=7)
app.register_blueprint(web)