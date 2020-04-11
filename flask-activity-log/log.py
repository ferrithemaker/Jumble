import os
import sqlite3
from flask import Flask,g
import log_db # local log_db.py
import log_auth # local log_auth.py
import log_blog # local log_blog.py

app = Flask(__name__)

app.config.from_mapping(SECRET_KEY='dev',DATABASE='/var/www/webapp/log.sqlite')
#print(app.instance_path)
#print(app.config['DATABASE'])


app.teardown_appcontext(log_db.close_db)

@app.route('/hello')
def hello():
        return 'Hello, World!'

app.register_blueprint(log_auth.bp)
app.register_blueprint(log_blog.bp)
app.add_url_rule('/', endpoint='index')
