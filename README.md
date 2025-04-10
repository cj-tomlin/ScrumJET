# ScrumJET

ScrumJET is an online training course platform specializing in Scrum and Agile methodology courses. This is version 2 of the application, rebuilt with modern technologies.

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

1. Clone the repository:
   ```
   git clone https://github.com/cj-tomlin/ScrumJET-v2.git
   cd ScrumJET-v2
   ```

2. Install Poetry if you haven't already:
   ```
   # On Windows
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

   # On macOS/Linux
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies and set up the project:
   ```
   make setup-dev # Install Poetry dependencies and pre-commit hooks
   make build     # Build Docker containers
   make init      # Start containers, initialize DB, and load sample data
   ```

   This will:
   - Install Poetry dependencies
   - Build and start Docker containers
   - Initialize the database
   - Apply migrations
   - Load sample data

4. Access the application at http://localhost:5000

## Available Make Commands

The project includes a Makefile with common commands to simplify development:

```
make setup      # Install Poetry dependencies
make setup-dev  # Setup development environment with pre-commit hooks
make build      # Build Docker containers
make up         # Start Docker containers
make down       # Stop Docker containers
make db-init    # Initialize the database
make db-migrate # Create a database migration (use message="Your message")
make db-upgrade # Apply database migrations
make load-data  # Load sample data
make logs       # View Docker logs
make shell      # Access shell in web container
make init       # Initialize everything (start containers, setup DB, load data)
make format     # Format code with ruff
make lint       # Lint code with ruff
make install-hooks # Install pre-commit hooks
make run-hooks    # Run pre-commit hooks on all files
make help       # Show all available commands
```


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
make db-migrate message="Description of changes"
make db-upgrade
```

### Running Tests

*Note: Tests will be added in the future.*

### Code Formatting and Linting

The project uses [ruff](https://github.com/charliermarsh/ruff) for code formatting and linting, configured with pre-commit hooks:

```
# Install pre-commit hooks
make install-hooks

# Run pre-commit hooks manually on all files
make run-hooks

# Format code with ruff
make format

# Lint code with ruff
make lint
```

## Deployment

### Docker

The application is configured for Docker deployment:

1. For production deployment, you may want to modify the environment variables in docker-compose.yml:
   ```
   FLASK_ENV=production
   FLASK_DEBUG=0
   ```

2. Build and deploy the Docker containers:
   ```
   make build
   make up
   ```

3. Initialize the database (if needed):
   ```
   make db-upgrade
   ```

### Planned Improvements

- Adding comprehensive test suite

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Original ScrumJET project developed as a university group project
- Bootstrap for the UI components
- Flask and its extensions for the backend functionality
