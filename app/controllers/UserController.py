# from flask import render_template, request, redirect, url_for, flash, session, abort
# from app import app

# from functools import wraps

# from app.services.UserService import UserService

# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#        if 'logged' in session:
#            return f(*args, **kwargs)
#        else:
#            flash('Vous devez être connecté pour accéder à cette page.', 'danger')
#            return redirect(url_for('login'))
#     return wrap

# def reqrole(*roles):
#     def wrap(f):
#         @wraps(f)
#         def verifyRole(*args, **kwargs):
#             if not session.get('logged'):
#                 return redirect(url_for('login'))
            
#             current_role = session.get('role')
#             if current_role not in  roles:
#                 abort(403)  # Forbidden
#             return f(*args, **kwargs)
#         return verifyRole
#     return wrap


# us = UserService()

# class LoginController:
#     @app.route('/login', methods=['GET', 'POST'])
#     def login():
#         msg_error = None
#         if request.method =='POST':
#             user = us.login(request.form['username'], request.form['password'])
#             if user:
#                 session['logged'] = True
#                 session['user_id'] = user.id
#                 session['username'] = user.username
#                 session['role'] = user.role
#                 return redirect(url_for('index'))

#             else:
#                msg_error = "Nom d'utilisateur ou mot de passe incorrect."
#         return render_template('login.html', msg_error=msg_error,metadata={'title': 'Connexion', 'pagename': 'login'})
    
#     @app.route('/register', methods=['GET', 'POST'])
#     def register():

#         if request.method == 'POST':
#             result = us.register(request.form['username'], request.form['password'])
#             if result:
#                 session["logged"] = True
#                 session['user_id'] = result.id
#                 session["username"] = request.form['username']
#                 session["role"] = 'lecteur'
#                 return redirect(url_for('index'))
#             else:
#                 flash("Le nom d'utilisateur est déjà utilisé.", 'danger')
#                 return render_template('register.html', metadata={'title': 'Inscription', 'pagename': 'register'}, msg_error="Le nom d'utilisateur est déjà utilisé.")
#         else:
#             return render_template('register.html', metadata={'title': 'Inscription', 'pagename': 'register'}, msg_error=None)

#     @app.route('/logout')
#     @login_required
#     def logout():
#         session.clear()
#         flash('Vous avez été déconnecté avec succès.', 'success')
#         return redirect(url_for('login'))
from flask import request, jsonify, session, abort
from flask import Blueprint
from functools import wraps
from app.services.UserService import UserService
from app import app, limiter

# ─── Décorateurs ────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged' in session:
            return f(*args, **kwargs)
        return jsonify({"error": "Connectez-vous pour accéder à cette page"}), 401
    return wrap

def reqrole(*roles):
    def wrap(f):
        @wraps(f)
        def verifyRole(*args, **kwargs):
            if not session.get('logged'):
                return jsonify({"error": "Non connecté"}), 401
            if session.get('role') not in roles:
                return jsonify({"error": "Accès interdit"}), 403
            return f(*args, **kwargs)
        return verifyRole
    return wrap

# ─── Controller ─────────────────────────────────────────────

us = UserService()

class UserController:
    def __init__(self):
        self.blueprint = Blueprint("auth", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/login",    view_func=self.login,    methods=["POST"])
        self.blueprint.add_url_rule("/register", view_func=self.register, methods=["POST"])
        self.blueprint.add_url_rule("/logout",   view_func=self.logout,   methods=["POST"])
        self.blueprint.add_url_rule("/me",       view_func=self.me,       methods=["GET"])
    @limiter.limit("5 per minute; 20 per hour; 50 per day")  # Limite à 5 tentatives de connexion par minute
    def login(self):
        data     = request.json or {}
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({"error": "Champs manquants"}), 400

        user = us.login(username, password)
        if user:
            session['logged']   = True
            session['user_id']  = user.id
            session['username'] = user.username
            session['role']     = user.role
            return jsonify({
                "success": True,
                "user": {
                    "id":       user.id,
                    "username": user.username,
                    "role":     user.role
                }
            })
        return jsonify({"error": "Identifiants incorrects"}), 401
    @limiter.limit("3 per minute; 10 per hour")  # Limite à 3 tentatives d'inscription par minute
    def register(self):
        data     = request.json or {}
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({"error": "Champs manquants"}), 400

        result = us.register(username, password)
        if result:
            session['logged']   = True
            session['user_id']  = result.id
            session['username'] = username
            session['role']     = 'lecteur'
            return jsonify({
                "success": True,
                "user": {
                    "id":       result.id,
                    "username": username,
                    "role":     "lecteur"
                }
            }), 201
        return jsonify({"error": "Nom d'utilisateur déjà utilisé"}), 409

    def logout(self):
        session.clear()
        return jsonify({"success": True, "message": "Déconnecté"})

    def me(self):
        return jsonify({
            "id":       session.get('user_id'),
            "username": session.get('username'),
            "role":     session.get('role')
        })

ctrl = UserController()