from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
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


@app.route('/')
def index():
    user_logged_in = False
    return render_template('index.html', user_logged_in=user_logged_in)


@app.route('/login')
def login():
    print(request)
    user_email = request.args['email']
    user_password = request.args['password']
    # user is an object returned from PG
    user = Registration.query.filter_by(email=user_email).first()
    email = user.email
    password = user.password
    print(email)
    print(password)
    if user_email == email and user_password == password:
        return render_template('index.html', user_logged_in=True, message="logged in")
    else:
        return render_template('index.html', user_logged_in=False, message="Error logging in")


@app.route('/signupform')
def signupform():
    return render_template('signup_form.html')


@app.route('/signup')
def signup():
    user_email = request.args['email']
    user_password = request.args['password']
    new_user = Registration(id=2, email=user_email, password=user_password)
    db.session.add(new_user)
    db.session.commit()
    return render_template('index.html', message="You are registered!")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
