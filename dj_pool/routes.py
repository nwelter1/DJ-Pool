from dj_pool import app, db, Message, mail
from flask import render_template, request, redirect, url_for
from dj_pool.forms import UserInfoForm, BlogPostForm, LoginForm, SongPostForm
from dj_pool.models import User, Post, SongPost, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
# Home Route
@app.route('/')
def home():
    return render_template("home.html")

# Blog route
@app.route('/blog')
def blog():
    posts = Post.query.all()
    return render_template('blog.html', posts=posts)

#Song Pool Route
@app.route('/songpool')
@login_required
def songpool():
    songs = SongPost.query.all()
    return render_template('songpool.html', songs=songs)

#Your Profile route
@app.route('/yourprofile')
@login_required
def yourprofile():
    songs = SongPost.query.all()
    posts = Post.query.all()
    return render_template('yourprofile.html', songs=songs,posts=posts)
# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n", username, password, email)
        #Create User instance
        user = User(username,email,password)
        #Open and insert into db
        db.session.add(user)
        db.session.commit()
        #Email sender
        msg = Message(f'Thanks for signing up, {username}!', recipients=[email])
        msg.body = ('Congrats on your new DJ Pool account! Looking forward to seeing your posts!')
        msg.html = ('<h1>Welcome to The Chicago DJ Pool</h1>' '<p>You can now access and post to the blog and music database!</p>')
        mail.send(msg)
    return render_template('register.html', form=form)

#Login Route
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

# Create a blog post
@app.route('/createapost', methods=['GET', 'POST'])
@login_required
def createapost():
    form = BlogPostForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        post = form.post.data
        user_id = current_user.id
        post_content = Post(title, post, user_id)

        db.session.add(post_content)
        db.session.commit()
        return redirect(url_for('createapost'))
    return render_template("createapost.html", form=form)

# Retrieve Method for Posts
@app.route('/posts/<int:post_id>')
@login_required
def post_detail(post_id):
    post_content = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post_content=post_content)

# Update Method for Posts
@app.route('/posts/update/<int:post_id>', methods=['GET','POST'])
@login_required
def post_update(post_id):
    post_content = Post.query.get_or_404(post_id)
    update_form = BlogPostForm()

    if request.method =='POST' and update_form.validate():
        title = update_form.title.data
        post = update_form.post.data
        user_id = current_user.id
        
        #Update post with form info
        post_content.title = title
        post_content.post = post
        post_content.user_id = user_id

        #commit
        db.session.commit()
        return redirect(url_for('post_update', post_id=post_id))


    return render_template('post_update.html', update_form=update_form)

# Create a Song Post Route 
@app.route('/createasong', methods=['GET',"POST"])
@login_required
def createasong():
    form = SongPostForm()
    if request.method == 'POST' and form.validate():
        song = form.song.data
        artist = form.artist.data
        bpm = form.bpm.data
        key = form.key.data
        download = form.download.data
        user_id = current_user.id
        post = SongPost(song, artist, bpm, key, download, user_id)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('createasong'))
        print('\n', song, artist, bpm, key, download)
    return render_template('createasong.html', form =form)

# Retreve Method for Songs
@app.route('/songs/<int:post_id>')
@login_required
def song_detail(post_id):
    post = SongPost.query.get_or_404(post_id)
    return render_template('song_detail.html', post=post)

# Update Method for Songs
@app.route('/songs/update/<int:post_id>', methods=['GET','POST'])
@login_required
def song_update(post_id):
    post = SongPost.query.get_or_404(post_id)
    song_update = SongPostForm()
    if request.method =='POST' and song_update.validate():
        song = song_update.song.data
        artist = song_update.artist.data
        bpm = song_update.bpm.data
        key = song_update.key.data
        user_id = current_user.id

        #Update
        post.song = song
        post.artist = artist
        post.bpm = bpm
        post.key = key
        post.user_id = user_id
        db.session.commit()
        return redirect(url_for('song_update', post_id=post_id))


    return render_template('song_update.html', song_update=song_update)

#log out route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))