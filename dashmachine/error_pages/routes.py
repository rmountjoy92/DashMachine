from flask import Blueprint, render_template

error_pages = Blueprint("error_pages", __name__)


# ------------------------------------------------------------------------------
# Error Pages
# ------------------------------------------------------------------------------
@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template("/error_pages/404.html"), 404


@error_pages.app_errorhandler(403)
def error_403(error):
    return render_template("/error_pages/403.html"), 403


@error_pages.app_errorhandler(500)
def error_500(error):
    return render_template("/error_pages/500.html"), 500


@error_pages.route("/unauthorized")
def unauthorized():
    return render_template("/error_pages/unauthorized.html")
