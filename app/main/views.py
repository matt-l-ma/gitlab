from flask import render_template, session, redirect, url_for, current_app
from . import main
from .. import auth

@main.route('/', methods=['GET'])
def index():
    return redirect(url_for('admin.index'))


