from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired

import os
import datetime as dt

SECRET_KEY = os.urandom(32)

PRIORITY = ("Choose...", "Critical", "High", "Medium", "Low")
STATUS = ("Choose...", "Not started", "In Progress", "In Review", "Completed", "Canceled")


# Setup Form Model
class ContactForm(FlaskForm):
    # Text
    title = StringField(
        label="title",
        validators=[DataRequired()],
        render_kw={"placeholder": "title"})
    description = StringField(
        label="description",
        validators=[DataRequired()],
        render_kw={"placeholder": "description"})

    # Dropdowns
    priority = SelectField(
        label="priority",
        choices=[(prio, prio) for prio in PRIORITY],
        validators=[DataRequired()],
        render_kw={"placeholder": "priority"})
    status = SelectField(
        label="status",
        choices=[(stat, stat) for stat in STATUS],
        validators=[DataRequired()],
        render_kw={"placeholder": "status"})
    submit = SubmitField("Add Task")


app = Flask(__name__)
app.secret_key = SECRET_KEY

# Connnect to SQL db
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # Postgres
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo_list.db')  # SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# TODO - Login Manager
# TODO - Admin User


# Setup Tables in db
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


# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    # POST
    if form.validate_on_submit():  # if New Added Task
        # Create new task
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            status=form.status.data
        )

        # Update db
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))

    # GET
    # Read all from task table in db
    all_tasks = db.session.query(Task).all()
    return render_template("index.html", tasks=all_tasks, form=form)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
