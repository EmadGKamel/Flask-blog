from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request, abort
from blog import app, forms, db, crypto, models, helpers


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = forms.PostForm()
    page = request.args.get('page', 1, type=int)
    posts = models.Post.query.order_by(models.Post.date.desc()).paginate(page=page, per_page=5)
    if form.validate_on_submit():
        post = models.Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('The Post has been publish', 'success')
        return redirect(url_for('home'))
    return render_template('index.html', posts=posts, form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed = crypto.generate_password_hash(form.password.data).decode('utf-8')
        user = models.User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash(u'Account created for {0}, Please login!'.format(form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('reg.html', title='register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and crypto.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            page = request.args.get('next')
            return redirect(page) if page else redirect(url_for('home'))
        else:
            flash('Incorrect Username or Password', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = forms.ProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image = helpers.save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile has been updated', 'success')
        return redirect(url_for('profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename='images/{0}'.format(current_user.image))
    return render_template('profile.html', title='profile', image=image, form=form)


@app.route('/post/<int:story>', methods=['GET', 'POST'])
def post(story):
    post = models.Post.query.get_or_404(story)
    if request.method == "POST":
        return redirect(url_for('home'))
    return render_template('post.html', title=post.title, post=post)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.RequestResetForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        helpers.send_reset_email(user)
        flash('An Email has been sent with reset link!', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = models.User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        hashed = crypto.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed
        db.session.commit()
        flash(u'Password has been updated, Please login!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route('/testin')
def user_wall():
    abort(400)
