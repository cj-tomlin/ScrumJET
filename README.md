# ScrumJET v2

ScrumJET is an online training course platform specializing in Scrum and Agile methodology courses. This is version 2 of the application, rebuilt from scratch with modern technologies.

## Features

- User authentication system (registration, login, password reset)
- Course management (listing, details, search, admin interface)
- Review system (ratings, comments)
- Blog/article system
- Events management
- User profiles with avatars and course progress tracking
- Mock payment system
- Course certificates generation
- Enhanced admin dashboard with analytics

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: Bootstrap 5 with Alpine.js for interactivity
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Email**: Flask-Mail
- **File Uploads**: Flask-Uploads
- **Migrations**: Flask-Migrate with Alembic
- **Dependency Management**: Poetry

## Installation

### Using Poetry

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ScrumJET-v2.git
   cd ScrumJET-v2
   ```

2. Install Poetry if you haven't already:
   ```
   # On Windows
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

   # On macOS/Linux
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies:
   ```
   poetry install
   ```

4. Activate the virtual environment:
   ```
   poetry shell
   ```

5. Set up PostgreSQL:
   - Install PostgreSQL if you haven't already
   - Create a database named `scrumjet_dev`
   - Update the `.env` file with your database credentials

6. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. Load sample data (optional):
   ```
   python scripts/init_db.py
   ```

8. Run the application:
   ```
   flask run
   ```

9. Access the application at http://localhost:5000

### Alternative: Using venv

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ScrumJET-v2.git
   cd ScrumJET-v2
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Follow steps 5-9 from the Poetry installation instructions above.

## Development

### Adding Dependencies

With Poetry:
```
poetry add package-name
poetry add package-name --dev  # For development dependencies
```

### Database Migrations

After making changes to the models, create a new migration:

```
flask db migrate -m "Description of changes"
flask db upgrade
```

### Running Tests

```
pytest
```

### Code Formatting

```
black app
```

## Deployment

### Docker

1. Build the Docker image:
   ```
   docker build -t scrumjet .
   ```

2. Run the container:
   ```
   docker run -p 5000:5000 scrumjet
   ```

### Heroku

1. Create a Heroku app:
   ```
   heroku create scrumjet
   ```

2. Add PostgreSQL addon:
   ```
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. Set environment variables:
   ```
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_APP=run.py
   ```

4. Deploy:
   ```
   git push heroku main
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Original ScrumJET project developed as a university group project
- Bootstrap for the UI components
- Flask and its extensions for the backend functionality