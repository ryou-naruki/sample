from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# ログインマネージャーのセットアップ
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ダミーユーザーモデル
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

users = {'1': {'username': 'user1', 'password': 'password1'},
        '2': {'username': 'user2', 'password': 'password2'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# ログインフォーム
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = None
        for uid, user in users.items():
            if user['username'] == form.username.data and user['password'] == form.password.data:
                user_id = uid
                break
        if user_id:
            user = User(user_id)
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# ダッシュボード
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.id}! Welcome to the dashboard.'

# ログアウト
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
