from app import app
from flask import render_template

from flask_login import login_required

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/about')
@login_required
def AboutStore():
    return render_template('about.html')
@app.route('/testing')  
def test():
     return 'This is a test'