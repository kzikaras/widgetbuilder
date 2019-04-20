from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import os
app = Flask(__name__)

app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Halothedog123@localhost/logmein',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

# create the registration table


class Registration(db.Model):
    __tablename__ = 'registration'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String, nullable=False)


class Widget(db.Model):
    __tablename__ = 'widget'
    widget_id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=False)


@app.route('/')
def index():
    if 'user_email' in session.keys():
        print(session)
        user_logged_in = True
        widgets = Widget.query.filter_by(reg_id=session['user_id']).all()
        print(widgets)
    else:
        widgets = []
        user_logged_in = False
    return render_template('index.html', user_logged_in=user_logged_in, widgets=widgets)


@app.route('/login')
def login():
    print(request)
    user_email = request.args['email']
    user_password = request.args['password']
    try:
        # user is an object returned from PG
        user = Registration.query.filter_by(email=user_email).first()
    except:
        return render_template('index.html', user_logged_in=False, message="Error logging in")
    email = user.email
    password = user.password
    print(email)
    print(password)
    if user_email == email and sha256_crypt.verify(user_password, password):
        session['user_email'] = user_email
        session['user_id'] = user.id
        session['logged_in'] = True
        print(session)
        widgets = Widget.query.filter_by(reg_id=session['user_id']).all()
        return render_template('index.html', user_logged_in=session['logged_in'], message="logged in", widgets=widgets)
    else:
        return render_template('index.html', user_logged_in=session['logged_in'], message="Error logging in")


@app.route('/logout')
def logout():
    session.clear()
    print(session)
    user_logged_in = False
    return render_template('index.html', user_logged_in=user_logged_in)


@app.route('/signupform')
def signupform():
    return render_template('signup_form.html')


@app.route('/signup')
def signup():
    user_email = request.args['email']
    user_password = sha256_crypt.encrypt(request.args['password'])
    new_user = Registration(email=user_email, password=user_password)
    db.session.add(new_user)
    db.session.commit()
    return render_template('index.html', message="You are registered!")


@app.route('/widget')
def widgetform():
    return render_template('widget_form.html')


@app.route('/create_widget')
def create_widget():
    new_widget = Widget(
        description=request.args['description'], reg_id=session['user_id'])
    db.session.add(new_widget)
    db.session.commit()
    widgets = Widget.query.filter_by(reg_id=session['user_id']).all()
    return render_template('index.html', user_logged_in=session['logged_in'], message="Widget created successfully!", widgets=widgets)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
