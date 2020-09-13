from dj_pool import app
from flask import render_template
from dj_pool.forms import UserInfoForm

# Home Route
@app.route('/')
def home():
    return render_template("home.html")

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserInfoForm()
    return render_template('register.html', form=form)