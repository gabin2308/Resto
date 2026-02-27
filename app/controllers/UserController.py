from flask import render_template, request, redirect, url_for, flash, session, abort
from app import app

from functools import wraps

from app.services.UserService import UserService

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
       if 'logged' in session:
           return f(*args, **kwargs)
       else:
           flash('Vous devez être connecté pour accéder à cette page.', 'danger')
           return redirect(url_for('login'))
    return wrap

def reqrole(*roles):
    def wrap(f):
        @wraps(f)
        def verifyRole(*args, **kwargs):
            if not session.get('logged'):
                return redirect(url_for('login'))
            
            current_role = session.get('role')
            if current_role not in  roles:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return verifyRole
    return wrap


us = UserService()

class LoginController:
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        msg_error = None
        if request.method =='POST':
            user = us.login(request.form['username'], request.form['password'])
            if user:
                session['logged'] = True
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                return redirect(url_for('index'))

            else:
               msg_error = "Nom d'utilisateur ou mot de passe incorrect."
        return render_template('login.html', msg_error=msg_error,metadata={'title': 'Connexion', 'pagename': 'login'})
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():

        if request.method == 'POST':
            result = us.register(request.form['username'], request.form['password'])
            if result:
                session["logged"] = True
                session['user_id'] = result.id
                session["username"] = request.form['username']
                session["role"] = 'lecteur'
                return redirect(url_for('index'))
            else:
                flash("Le nom d'utilisateur est déjà utilisé.", 'danger')
                return render_template('register.html', metadata={'title': 'Inscription', 'pagename': 'register'}, msg_error="Le nom d'utilisateur est déjà utilisé.")
        else:
            return render_template('register.html', metadata={'title': 'Inscription', 'pagename': 'register'}, msg_error=None)

    @app.route('/logout')
    @login_required
    def logout():
        session.clear()
        flash('Vous avez été déconnecté avec succès.', 'success')
        return redirect(url_for('login'))