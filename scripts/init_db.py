import os
import sys
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import (
    User, Category, Course, Announcement, FAQ, Article, ArticleCategory,
    Event, Sponsor, CourseModule, CourseLesson
)

def create_sample_data():
    """Create sample data for the application."""
    app = create_app('development')
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if we already have data
        if User.query.count() > 0:
            print("Database already contains data. Skipping sample data creation.")
            return
        
        print("Creating sample data...")
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@scrumjet.com',
            first_name='Admin',
            last_name='User',
            role=User.ROLE_ADMIN,
            admin=True,
            email_confirmed=True,
            email_confirmed_at=datetime.utcnow()
        )
        admin.set_password('adminpass')
        db.session.add(admin)
        
        # Create regular user
        user = User(
            username='user',
            email='user@example.com',
            first_name='Regular',
            last_name='User',
            role=User.ROLE_USER,
            email_confirmed=True,
            email_confirmed_at=datetime.utcnow()
        )
        user.set_password('userpass')
        db.session.add(user)
        
        # Create trainer user
        trainer = User(
            username='trainer',
            email='trainer@scrumjet.com',
            first_name='Scrum',
            last_name='Trainer',
            role=User.ROLE_TRAINER,
            is_cst=True,
            bio='Certified Scrum Trainer with over 10 years of experience in Agile methodologies.',
            email_confirmed=True,
            email_confirmed_at=datetime.utcnow()
        )
        trainer.set_password('trainerpass')
        db.session.add(trainer)
        
        # Create categories
        certified = Category(name='Certified Courses')
        non_certified = Category(name='Non-Certified Courses')
        workshops = Category(name='Workshops')
        db.session.add_all([certified, non_certified, workshops])
        
        # Create courses
        course1 = Course(
            title='Certified ScrumMaster (CSM)',
            summary='Learn the Scrum framework and gain an understanding of team roles, events, and artifacts.',
            description='This two-day course provides a comprehensive introduction to the Scrum framework, including its roles, events, and artifacts. You will learn how to apply Scrum in your organization and gain the knowledge to become a Certified ScrumMaster.',
            price=995.00,
            duration=16,  # 16 hours (2 days)
            level='Beginner',
            category=certified,
            creator=trainer
        )
        
        course2 = Course(
            title='Advanced Scrum Master',
            summary='Take your Scrum Master skills to the next level with advanced techniques and practices.',
            description='This advanced course is designed for experienced Scrum Masters who want to deepen their knowledge and skills. You will learn advanced facilitation techniques, coaching skills, and how to scale Scrum in large organizations.',
            price=1295.00,
            duration=24,  # 24 hours (3 days)
            level='Advanced',
            category=certified,
            creator=trainer
        )
        
        course3 = Course(
            title='Agile Fundamentals',
            summary='Introduction to Agile methodologies and principles.',
            description='This course provides a solid foundation in Agile methodologies, including Scrum, Kanban, and XP. You will learn the principles and values of Agile and how to apply them in your projects.',
            price=495.00,
            duration=8,  # 8 hours (1 day)
            level='Beginner',
            category=non_certified,
            creator=trainer
        )
        
        db.session.add_all([course1, course2, course3])
        
        # Create course modules and lessons for the first course
        module1 = CourseModule(
            title='Introduction to Scrum',
            description='Learn the basics of Scrum and its history.',
            order=1,
            course=course1
        )
        
        lesson1_1 = CourseLesson(
            title='What is Scrum?',
            content='Scrum is an agile framework for developing, delivering, and sustaining complex products...',
            order=1,
            duration=60,  # 60 minutes
            module=module1
        )
        
        lesson1_2 = CourseLesson(
            title='Scrum History',
            content='Scrum was first defined as a formal process in 1995 by Ken Schwaber and Jeff Sutherland...',
            order=2,
            duration=45,  # 45 minutes
            module=module1
        )
        
        module2 = CourseModule(
            title='Scrum Roles',
            description='Learn about the three roles in Scrum: Product Owner, Scrum Master, and Development Team.',
            order=2,
            course=course1
        )
        
        lesson2_1 = CourseLesson(
            title='The Product Owner',
            content='The Product Owner is responsible for maximizing the value of the product...',
            order=1,
            duration=60,  # 60 minutes
            module=module2
        )
        
        lesson2_2 = CourseLesson(
            title='The Scrum Master',
            content='The Scrum Master is responsible for promoting and supporting Scrum...',
            order=2,
            duration=60,  # 60 minutes
            module=module2
        )
        
        lesson2_3 = CourseLesson(
            title='The Development Team',
            content='The Development Team consists of professionals who do the work of delivering a potentially releasable Increment...',
            order=3,
            duration=60,  # 60 minutes
            module=module2
        )
        
        db.session.add_all([module1, lesson1_1, lesson1_2, module2, lesson2_1, lesson2_2, lesson2_3])
        
        # Create announcements
        announcement1 = Announcement(
            title='New Certified Courses Available',
            body='We are excited to announce the launch of our new certified Scrum courses. Check them out and enroll today!'
        )
        
        announcement2 = Announcement(
            title='Platform Maintenance',
            body='ScrumJET will be undergoing maintenance on Saturday, May 15th from 2:00 AM to 4:00 AM UTC. The platform may be unavailable during this time.'
        )
        
        db.session.add_all([announcement1, announcement2])
        
        # Create FAQs
        faq1 = FAQ(
            question='What is Scrum?',
            answer='Scrum is an agile framework for developing, delivering, and sustaining complex products. It is designed for teams of ten or fewer members, who break their work into goals that can be completed within timeboxed iterations, called sprints.'
        )
        
        faq2 = FAQ(
            question='How do I get certified?',
            answer='To get certified, you need to attend one of our certified courses and pass the certification exam. The exam is typically taken online after the course.'
        )
        
        faq3 = FAQ(
            question='What is the difference between Scrum and Agile?',
            answer='Agile is a set of principles and values, while Scrum is a specific framework that implements Agile principles. Scrum is one of several Agile frameworks, along with Kanban, XP, and others.'
        )
        
        db.session.add_all([faq1, faq2, faq3])
        
        # Create article categories
        agile_cat = ArticleCategory(name='Agile', description='Articles about Agile methodologies and principles')
        scrum_cat = ArticleCategory(name='Scrum', description='Articles about the Scrum framework')
        kanban_cat = ArticleCategory(name='Kanban', description='Articles about the Kanban method')
        
        db.session.add_all([agile_cat, scrum_cat, kanban_cat])
        
        # Create articles
        article1 = Article(
            title='The Benefits of Agile Methodologies',
            summary='Explore the many benefits of adopting Agile methodologies in your organization.',
            body='Agile methodologies have revolutionized the way teams work together to deliver value to customers...',
            author=admin,
            article_category=agile_cat,
            published=True,
            published_at=datetime.utcnow() - timedelta(days=5)
        )
        
        article2 = Article(
            title='Scrum vs. Kanban: Which is Right for Your Team?',
            summary='A comparison of Scrum and Kanban to help you choose the right framework for your team.',
            body='Both Scrum and Kanban are popular Agile frameworks, but they have different approaches and are suited to different types of work...',
            author=trainer,
            article_category=scrum_cat,
            published=True,
            published_at=datetime.utcnow() - timedelta(days=2)
        )
        
        db.session.add_all([article1, article2])
        
        # Create events
        event1 = Event(
            name='Scrum Master Certification Workshop',
            description='A two-day workshop to prepare for the Certified ScrumMaster exam.',
            start_date=datetime.utcnow() + timedelta(days=30),
            end_date=datetime.utcnow() + timedelta(days=32),
            venue_name='ScrumJET Training Center',
            venue_address='123 Agile Street, London, UK',
            organizer=trainer
        )
        
        event2 = Event(
            name='Agile Leadership Summit',
            description='A one-day summit for leaders to learn how to foster Agile culture in their organizations.',
            start_date=datetime.utcnow() + timedelta(days=45),
            end_date=datetime.utcnow() + timedelta(days=46),
            venue_name='Grand Hotel',
            venue_address='456 Main Street, London, UK',
            organizer=admin
        )
        
        db.session.add_all([event1, event2])
        
        # Create sponsors
        sponsor1 = Sponsor(
            name='Agile Alliance',
            website='https://www.agilealliance.org'
        )
        
        sponsor2 = Sponsor(
            name='Scrum.org',
            website='https://www.scrum.org'
        )
        
        db.session.add_all([sponsor1, sponsor2])
        
        # Commit the session
        db.session.commit()
        
        print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()