from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """Returns rendered template for 404 page when 404 error occurs."""
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """Returns rendered template for 403 page when 403 error occurs."""
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """Returns rendered template for 500 page when 500 error occurs."""
    return render_template('errors/500.html'), 500
