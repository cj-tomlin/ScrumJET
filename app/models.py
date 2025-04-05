import jwt
import os
from time import time
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property


# Timestamp mixin for automatic `created_at` and `updated_at` fields
class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Association table for user course enrollments
enrollments = db.Table('enrollments',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('enrolled_at', db.DateTime, default=datetime.utcnow),
    db.Column('completed', db.Boolean, default=False)
)


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
    
    # Email confirmation
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmed_at = db.Column(db.DateTime)
    
    # Profile fields
    avatar = db.Column(db.String(100))  # Path to avatar image
    bio = db.Column(db.Text)  # User biography
    location = db.Column(db.String(100))  # User location
    website = db.Column(db.String(100))  # User website
    
    # Social media links
    twitter = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))
    github = db.Column(db.String(100))
    
    # Extended profile fields for CSP and CST
    is_csp = db.Column(db.Boolean, default=False)  # Certified Scrum Practitioner
    is_cst = db.Column(db.Boolean, default=False)  # Certified Scrum Trainer
    
    # Relationships
    reviews = db.relationship('Review', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    events = db.relationship('Event', backref='organizer', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    trainer_ratings = db.relationship('TrainerRating', foreign_keys='TrainerRating.trainer_id', backref='trainer', lazy='dynamic')
    courses_created = db.relationship('Course', backref='creator', lazy='dynamic')
    payments = db.relationship('Payment', backref='user', lazy='dynamic')
    certificates = db.relationship('Certificate', backref='user', lazy='dynamic')
    
    # Course enrollments
    enrolled_courses = db.relationship('Course', secondary=enrollments, 
                                      backref=db.backref('enrolled_users', lazy='dynamic'),
                                      lazy='dynamic')
    
    # Module and lesson progress
    module_progress = db.relationship('ModuleProgress', backref='user', lazy='dynamic')
    lesson_progress = db.relationship('LessonProgress', backref='user', lazy='dynamic')

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
    
    # Generate an email confirmation token
    def get_confirmation_token(self, expires_in=86400):  # 24 hours
        return jwt.encode(
            {'confirm_email': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    # Verify the email confirmation token
    @staticmethod
    def verify_confirmation_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['confirm_email']
        except:
            return None
        return User.query.get(user_id)
    
    # Confirm email
    def confirm_email(self):
        self.email_confirmed = True
        self.email_confirmed_at = datetime.utcnow()
        db.session.add(self)
    
    # Enroll in a course
    def enroll_in_course(self, course):
        if not self.is_enrolled_in(course):
            self.enrolled_courses.append(course)
            db.session.add(self)
            return True
        return False
    
    # Check if enrolled in a course
    def is_enrolled_in(self, course):
        return self.enrolled_courses.filter(enrollments.c.course_id == course.id).count() > 0
    
    # Get full name
    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
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
    description = db.Column(db.String(200))
    courses = db.relationship('Course', backref='category', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Category {self.name}>'


# Course model
class Course(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    summary = db.Column(db.Text)
    description = db.Column(db.Text)
    image = db.Column(db.String(100))
    price = db.Column(db.Float, default=99.99)
    duration = db.Column(db.Integer)  # Duration in hours
    level = db.Column(db.String(20))  # Beginner, Intermediate, Advanced
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    reviews = db.relationship('Review', backref='course', lazy='dynamic', cascade="all, delete-orphan")
    modules = db.relationship('CourseModule', backref='course', lazy='dynamic', cascade="all, delete-orphan")
    certificates = db.relationship('Certificate', backref='course', lazy='dynamic')
    
    def __repr__(self):
        return f'<Course {self.title}>'
    
    # Calculate average rating
    @hybrid_property
    def average_rating(self):
        if self.reviews.count() == 0:
            return 0
        return sum(review.rating for review in self.reviews) / self.reviews.count()
    
    # Get total number of lessons
    @hybrid_property
    def total_lessons(self):
        total = 0
        for module in self.modules:
            total += module.lessons.count()
        return total


# Course Module model
class CourseModule(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)  # Order within the course
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Relationships
    lessons = db.relationship('CourseLesson', backref='module', lazy='dynamic', cascade="all, delete-orphan")
    progress = db.relationship('ModuleProgress', backref='module', lazy='dynamic')
    
    def __repr__(self):
        return f'<Module {self.title} for Course {self.course_id}>'


# Course Lesson model
class CourseLesson(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)  # Order within the module
    duration = db.Column(db.Integer)  # Duration in minutes
    module_id = db.Column(db.Integer, db.ForeignKey('course_module.id'), nullable=False)
    
    # Relationships
    progress = db.relationship('LessonProgress', backref='lesson', lazy='dynamic')
    
    def __repr__(self):
        return f'<Lesson {self.title} for Module {self.module_id}>'


# Module Progress model
class ModuleProgress(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('course_module.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ModuleProgress for User {self.user_id} on Module {self.module_id}>'


# Lesson Progress model
class LessonProgress(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('course_lesson.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LessonProgress for User {self.user_id} on Lesson {self.lesson_id}>'


# Payment model
class Payment(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    
    # Relationships
    course = db.relationship('Course', backref='payments')
    
    def __repr__(self):
        return f'<Payment {self.id} for Course {self.course_id} by User {self.user_id}>'


# Certificate model
class Certificate(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    certificate_number = db.Column(db.String(50), unique=True)
    verification_code = db.Column(db.String(50), unique=True)
    
    def __repr__(self):
        return f'<Certificate {self.certificate_number} for User {self.user_id}>'


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
    
    # Relationships
    registrations = db.relationship('EventRegistration', backref='event', lazy='dynamic')

    def __repr__(self):
        return f'<Event {self.name}>'


# Event Registration model
class EventRegistration(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    attended = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship('User', backref='event_registrations')
    
    def __repr__(self):
        return f'<EventRegistration for User {self.user_id} on Event {self.event_id}>'


# Article Category model
class ArticleCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(200))
    
    # Relationships
    articles = db.relationship('Article', backref='article_category', lazy='dynamic')
    
    def __repr__(self):
        return f'<ArticleCategory {self.name}>'


# Article model
class Article(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500))
    image = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # User as author
    category_id = db.Column(db.Integer, db.ForeignKey('article_category.id'))
    published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    
    # Relationships
    comments = db.relationship('Comment', backref='article', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Article {self.title}>'
    
    # Publish article
    def publish(self):
        self.published = True
        self.published_at = datetime.utcnow()
        db.session.add(self)


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # User who rated
    
    # Relationships
    rater = db.relationship('User', foreign_keys=[user_id], backref='ratings_given')

    def __repr__(self):
        return f'<Rating for Trainer {self.trainer_id}>'
