# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
from flask import Flask
from flask import request
from flask import jsonify
from flask import g

from flask_sqlalchemy import SQLAlchemy

from flask import abort

from passlib.apps import custom_app_context as pwd_context

from flask_httpauth import HTTPBasicAuth

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
auth = HTTPBasicAuth()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Activation du mode debogage
app.debug = True

# Configuration de la clé de sécurisation des sessions
app.secret_key = '2d9-E2.)f&é,A$p@fpa+zSU03êû9_'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=30):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            # valid token, but expired# valid token, but expired
            return None
        except BadSignature:
            # invalid token
            return None
        user = User.query.get(data['id'])
        return user


@app.route('/')
def index():
    return 'Hello !'

@app.route('/api/users', methods=['POST'])
@auth.login_required
def new_user():
    print('__Executing new user methode__')
    import pdb; pdb.set_trace()
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        # missing arguments
        abort(400, 'Username or password is empty')

    if User.query.filter_by(username = username).first() is not None:
        # existing user
        abort(401, 'This user already exists on the database')

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    #return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id = user.id, _external = True)}
    return jsonify({'username': user.username}), 201

@app.route('/api/resource')
@auth.login_required
def get_resource():
    print('__Executing get_resource methode__')
    return jsonify({'data': 'Hello, %s!' % g.user.username})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

"""
@auth.verify_password
def verify_password(username, password):
    print('__Executing verify_password methode__')
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True
"""

@auth.verify_password
def verify_password(username_or_token, password):
    #import pdb; pdb.set_trace()
    print('first try to authenticate by token')
    user = User.verify_auth_token(username_or_token)
    if not user:
        print('try to authenticate with username/password')
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# start the flask loop
if __name__ == '__main__':
    db.create_all()
    user = User()
    user.username = 'Admin'
    user.password = 'P@ssw0rd'
    db.session.add(user)
    db.session.commit()
    app.run()
