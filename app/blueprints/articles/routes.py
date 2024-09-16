from flask import Blueprint, render_template, redirect, url_for
from app.models import Article

articles_bp = Blueprint('articles', __name__)


@articles_bp.route('/articles')
def list_articles():
    articles = Article.query.all()
    return render_template('articles/article_list.html', articles=articles)


@articles_bp.route('/articles/<int:id>')
def article_detail(id):
    article = Article.query.get_or_404(id)
    return render_template('articles/article_detail.html', article=article)
