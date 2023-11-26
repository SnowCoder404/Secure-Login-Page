#
#   Copyright © 2023, SnowCoder404
#
import hashlib
import qrcode
import os
import pyotp
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
IMG_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
db = SQLAlchemy(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        salt_key = os.urandom(32).hex()
        key = two_factor(user=user)
        db.create_all()
        db_user = Data.query.filter_by(user=user).first()
        if db_user is None:
            db.create_all()
            private_key = import_key()
            public_key = private_key.public_key()
            crypt_token = encrypt(public_key=public_key, data=key)
            token = b64encode(crypt_token).decode()
            pw = hashing(pw=pw, salt=salt_key)
            crypt_pw = encrypt(public_key=public_key, data=pw)
            crypt_pw = b64encode(crypt_pw).decode()
            db.session.add(Data(user=user, pw=crypt_pw,  salt_key=str(salt_key), totp_key=token))
            db.session.commit()
            two_factor_qr(link=key, user=user)
            return render_template('qr.html', totp=IMG_FOLDER + '/' + key + '.png', user=user)
        else:
            return 'Username is not free'
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        db_user = Data.query.filter_by(user=user).first()
        if db_user is not None:
            private_key = import_key()
            pw = hashing(pw=pw, salt=db_user.salt_key)
            crypt_pw = decrypt(private_key=private_key, data=db_user.pw)
            if pw == crypt_pw:
                # All data correct
                return render_template('two-factor.html', user=user)
            else:
                return 'Username or Password is Wrong'
        else:
            return 'Username or Password is Wrong'
    return render_template('login.html')


@app.route('/totp', methods=['POST'])
def totp():
    if request.method == 'POST':
        user = request.form['user']
        totp_key = request.form['totp_key']
        db_user = Data.query.filter_by(user=user).first()
        private_key = import_key()
        token = decrypt(private_key=private_key, data=db_user.totp_key)
        totp_token = pyotp.TOTP(token)
        if totp_key == totp_token.now():
            return render_template('index.html', user=user)
        else:
            return render_template('two-factor.html', user=user)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), unique=True)
    pw = db.Column(db.String(200))
    salt_key = db.Column(db.String(200))
    totp_key = db.Column(db.String(200))


def hashing(salt, pw):
    salt = bytes(salt, encoding='utf-8')
    hashed_password = hashlib.sha512(salt + pw.encode() + salt)
    hashed_password = hashed_password.hexdigest().encode()
    return hashed_password.decode()


def two_factor(user):
    private_key = pyotp.random_base32()
    return private_key


def two_factor_qr(link, user):
    key = pyotp.totp.TOTP(link).provisioning_uri(name=user, issuer_name='SnowCoder404')
    qr_code = qrcode.make(data=key)
    qr_code.save(IMG_FOLDER + '/' + link + '.png')


def import_key():
    with open(IMG_FOLDER + '/' + 'secret_key.pem', 'rb') as f_in:
        private_key = RSA.import_key(f_in.read())
    return private_key


def encrypt(public_key, data):
    cipher = PKCS1_OAEP.new(public_key)
    data = bytes(data.encode())
    crypt_data = cipher.encrypt(data)
    return crypt_data


def decrypt(private_key, data):
    cipher = PKCS1_OAEP.new(private_key)
    decrypt_data = cipher.decrypt(b64decode(data))
    return decrypt_data.decode()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
    
