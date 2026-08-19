from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import alquimias


def init_app(app):

    @app.route('/')
    @app.route('/index')
    def index():
        posts = None
        if current_user.is_authenticated:
            posts = alquimias.get_timeline()
        return render_template('index.html', posts=posts)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = alquimias.get_user_by_username(username)
            if user is None or not user.check_password(password):
                flash('Usuário ou senha inválidos.')
                return redirect(url_for('login'))

            login_user(user)
            return redirect(url_for('index'))

        return render_template('login.html')

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            foto = request.form.get('foto') or None
            bio = request.form.get('bio') or None

            if alquimias.get_user_by_username(username):
                flash('Nome de usuário já em uso.')
                return redirect(url_for('cadastro'))

            alquimias.create_user(username, email, password, foto, bio)
            flash('Cadastro realizado! Faça login.')
            return redirect(url_for('login'))

        return render_template('cadastro.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/post', methods=['GET', 'POST'])
    @login_required
    def post():
        if request.method == 'POST':
            body = request.form.get('body')
            if body and body.strip():
                alquimias.create_post(body.strip(), current_user)
                return redirect(url_for('index'))
            flash('O post não pode ser vazio.')
            return redirect(url_for('post'))

        return render_template('post.html')
