from flask import Blueprint, render_template, request
from app.models import Article

articles_bp = Blueprint('articles', __name__)


# Existing route for listing articles
@articles_bp.route('/articles')
def list_articles():
    articles = Article.query.all()  # Fetch all articles by default
    categories = []  # Fetch categories for filtering
    return render_template('articles/article_list.html', articles=articles, categories=categories)


# Route for search functionality
@articles_bp.route('/articles/search')
def search():
    query = request.args.get('q', '').strip()  # Get the search query from the URL parameters
    if query:
        articles = Article.query.filter(Article.title.ilike(f'%{query}%') |
                                        Article.summary.ilike(f'%{query}%')).all()
    else:
        articles = []  # Return no articles if no search query is provided

    categories = []  # Fetch categories for filtering
    return render_template('articles/article_list.html', articles=articles, categories=categories, query=query)
