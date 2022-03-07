from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

import os
import datetime as dt

app = Flask(__name__)

# Connnect to SQL db
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # Postgres
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo_list.db')  # SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# TODO - Login Manager
# TODO - Admin User


# TODO - Setup Tables in db
class User(UserMixin, db.Model):  # Create Users Table Model
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100))

    tasks = db.relationship("Task", back_populates='author')


class Task(db.Model):  # Create Tasks Table Model
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', back_populates='tasks')

    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(30))
    priority = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=False)


# Create tables in db
db.create_all()


# TODO - Routes
@app.route("/", methods=["GET", "POST"])
def home():
    # POST
        # TODO - Receive Add Task btn pressed
        # TODO - Open Popup Window with form to add to table/db
        # return

    # GET
    # Read all from task table in db
    all_tasks = db.session.query(Task).all()
    return render_template("index.html", tasks=all_tasks)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
