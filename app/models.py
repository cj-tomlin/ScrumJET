import jwt
from time import time
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Timestamp mixin for automatic `created_at` and `updated_at` fields
class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User class with roles for access control
class User(db.Model, TimestampMixin, UserMixin):
    ROLE_USER = 0
    ROLE_ADMIN = 1
    ROLE_TRAINER = 2
    ROLE_EDITOR = 3

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)  # User roles for access control
    admin = db.Column(db.Boolean, default=False)  # Optional: Mark admin using boolean
    reviews = db.relationship('Review', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    events = db.relationship('Event', backref='organizer', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    trainer_ratings = db.relationship('TrainerRating', backref='trainer', lazy='dynamic')

    # Extended profile fields for CSP and CST
    is_csp = db.Column(db.Boolean, default=False)  # Certified Scrum Practitioner
    is_cst = db.Column(db.Boolean, default=False)  # Certified Scrum Trainer
    bio = db.Column(db.Text)  # For CSP and CST profiles

    def __repr__(self):
        return f'<User {self.username}>'

    # Password hashing and verification
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Generate a password reset token
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    # Verify the reset password token
    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(user_id)

    # Role checks
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_trainer(self):
        return self.role == self.ROLE_TRAINER

    def is_editor(self):
        return self.role == self.ROLE_EDITOR


# Announcement model with length constraints
class Announcement(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return f'<Announcement "{self.title}">'


# Category model with cascading delete for courses
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    courses = db.relationship('Course', backref='category', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Category {self.name}>'


# Course model
class Course(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    summary = db.Column(db.Text)
    image = db.Column(db.String(100))
    price = db.Column(db.Float, default=99.99)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    reviews = db.relationship('Review', backref='course', lazy='dynamic', cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Course {self.title}>'


# Review model
class Review(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __repr__(self):
        return f'<Review {self.id} for course {self.course_id}>'

    def validate_rating(self):
        if not (0.0 <= self.rating <= 5.0):
            raise ValueError('Rating must be between 0 and 5.')


# Event model
class Event(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    venue_name = db.Column(db.String(100))
    venue_address = db.Column(db.String(200))
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # User organizing the event

    def __repr__(self):
        return f'<Event {self.name}>'


# Article model
class Article(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # User as author
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    def __repr__(self):
        return f'<Article {self.title}>'


# Comment model for articles
class Comment(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __repr__(self):
        return f'<Comment by User {self.user_id} on Article {self.article_id}>'


# FAQ model
class FAQ(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return f'<FAQ "{self.question}">'


# Corporate Sponsor model
class Sponsor(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(100))  # Path to sponsor logo image
    website = db.Column(db.String(255))

    def __repr__(self):
        return f'<Sponsor {self.name}>'


# Trainer Rating model
class TrainerRating(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, default=0.0)
    review = db.Column(db.String(5000))  # Optional text review
    trainer_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Trainer being rated

    def __repr__(self):
        return f'<Rating for Trainer {self.trainer_id}>'
