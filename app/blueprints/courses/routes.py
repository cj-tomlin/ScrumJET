from flask import Blueprint, render_template
from app.models import Course

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses')
def list_courses():
    courses = Course.query.all()
    return render_template('courses/course_list.html', courses=courses)

@courses_bp.route('/courses/<int:id>')
def course_detail(id):
    course = Course.query.get_or_404(id)
    return render_template('courses/course_detail.html', course=course)