# ScrumJET Project Analysis and Rebuild Prompt

## Project Overview

ScrumJET is an online training course platform specializing in Scrum and Agile methodology courses. The application was originally developed as a university group project using the Scrum methodology, with team members rotating as Scrum Masters. The platform allows users to browse, search, and review courses, with administrative capabilities for course management.

## Technology Stack

- **Frontend**: HTML/CSS, Bootstrap 3, JavaScript/jQuery
- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Additional Libraries**: 
  - Flask-Login (authentication)
  - Flask-Mail (password reset)
  - Flask-Bootstrap (UI framework)
  - Flask-Moment (time formatting)
  - Flask-Paginate (pagination)
  - Raty.js (star rating system)

## Core Features and Implementation Status

### 1. User Authentication System ✅
- User registration with validation
- Login/logout functionality
- Password reset via email
- User roles (regular users and admins)

### 2. Course Management ✅
- Course listings with pagination
- Course details pages
- Course categories (certified/non-certified)
- Course search functionality
- Course images with upload capability
- Admin interface for adding/editing/deleting courses

### 3. Review System ✅
- Star ratings (1-5 stars)
- Text reviews
- Average rating calculation
- Edit/delete review functionality
- Prevention of multiple reviews by the same user

### 4. Frontend Design ✅
- Responsive Bootstrap-based design
- Custom CSS for styling
- Carousel on homepage
- Course cards with hover effects
- Footer with contact information and social media links

### 5. Additional Pages ✅
- About page
- FAQ page
- Contact page
- Terms & Conditions and Privacy Policy pages
- Sitemap

### 6. Blog System 🔄
- Blog templates exist
- Basic routes are defined
- Functionality appears to be partially implemented or placeholder

### 7. Announcements System ✅
- Admin can create announcements
- Announcements displayed on homepage

## Database Structure

The application uses five main models:
1. **User**: Authentication and profile information
   - Fields: id, username, email, password_hash, first_name, last_name, admin flag
   - Relationships: has many reviews, has many courses (if admin)

2. **Course**: Course details including title, summary, price, image
   - Fields: id, title, summary, image, price, category_id, user_id
   - Relationships: belongs to category, has many reviews, belongs to user (creator)

3. **Category**: Course categories (certified/non-certified)
   - Fields: id, name
   - Relationships: has many courses

4. **Review**: User reviews for courses with ratings
   - Fields: id, text, rating, user_id, course_id
   - Relationships: belongs to user, belongs to course

5. **Announcement**: System announcements for the homepage
   - Fields: id, title, body, created_at, updated_at

## Project Architecture

- **Flask Blueprint Structure**:
  - `auth`: Authentication-related routes and forms
  - `main`: General pages and navigation
  - `courses`: Course-related functionality
  - `errors`: Error handling

- **MVC Pattern**:
  - Models: SQLAlchemy models in `models.py`
  - Views: Jinja2 templates in `templates/` directory
  - Controllers: Route functions in blueprint route files

- **Template Inheritance**:
  - Base template with common elements (navbar, footer)
  - Page-specific templates extending the base

- **Static Assets**:
  - CSS files organized by page/component
  - JavaScript for interactive elements
  - Images for courses and UI elements

## Current Progress Assessment

The original ScrumJET application appears to be functionally complete with most core features implemented. The codebase is well-structured following Flask best practices with blueprints for modularity. The UI is polished with Bootstrap styling and custom CSS.

Areas that might need further development or enhancement:
1. The blog functionality appears to be partially implemented
2. Admin dashboard could be expanded with more analytics
3. Payment processing is not implemented (courses have prices but no checkout system)
4. User profiles could be enhanced with more features
5. Mobile responsiveness could be improved in some areas

## Rebuild Recommendations

For your portfolio rebuild, consider:

1. **Modernizing the tech stack**:
   - Upgrade to Bootstrap 5 or consider a more modern framework like Tailwind CSS
   - Consider using a modern JavaScript framework (React, Vue, or Alpine.js) for interactive components
   - Upgrade Flask dependencies to latest versions

2. **Enhancing existing features**:
   - Implement a complete blog system with categories and comments
   - Add a dashboard for users to track their courses
   - Implement a mock payment system for demonstration purposes

3. **Adding new features**:
   - User profiles with avatars and bios
   - Course progress tracking
   - Course certificates generation
   - Related courses recommendations
   - Course filtering by multiple criteria

4. **Improving UX/UI**:
   - Modernize the design while maintaining the brand identity
   - Enhance accessibility features
   - Improve mobile experience
   - Add dark mode support

5. **DevOps considerations**:
   - Containerize the application with Docker
   - Add comprehensive testing
   - Set up CI/CD pipeline
   - Consider deploying to a cloud platform

## Technical Implementation Details

### Authentication Flow
- Registration form with validation
- Password hashing using Werkzeug's security functions
- JWT-based password reset tokens
- Flask-Login for session management

### Database Relationships
- One-to-many relationship between User and Review
- One-to-many relationship between Course and Review
- One-to-many relationship between Category and Course
- One-to-many relationship between User and Course (for course creators)

### Form Handling
- WTForms for form creation and validation
- CSRF protection
- File uploads for course images

### Frontend Components
- Bootstrap grid system for responsive layout
- jQuery for DOM manipulation
- Raty.js for star ratings
- Moment.js for time formatting

This analysis should provide a solid foundation for assessing your current rebuild progress and planning the next steps for your portfolio project.