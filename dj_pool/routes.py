from dj_pool import app
from flask import render_template

# Home Route
@app.route('/')
def home():
    return render_template("home.html")