from flask import Blueprint, render_template
from flask_login.utils import login_required

site = Blueprint('site', __name__, template_folder='site_templates')

"""
Note that in the above code some arguments are specified the Blueprint object.
The first argument, 'site':
    The Blueprint's name, which is used by Flask's routing mechanism.
The second argument, __name__:
    The Blueprint's import name, which Flask uses to locate the Blueprint's resource
"""

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')