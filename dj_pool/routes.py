from dj_pool import app
from flask import render_template, request
from dj_pool.forms import UserInfoForm, BlogPostForm

# Home Route
@app.route('/')
def home():
    return render_template("home.html")

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n", username, password, email)
    return render_template('register.html', form=form)

# Create a blog post
@app.route('/createapost', methods=['GET', 'POST'])
def createapost():
    form = BlogPostForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        post = form.post.data
        print('\n', title, post)
    return render_template("createapost.html", form=form)

