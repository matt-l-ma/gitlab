from flask import render_template, redirect, url_for,request, flash, session
from flask_security import login_user, login_required, current_user, logout_user
from flask_admin import helpers, expose, AdminIndexView
from flask_admin.contrib import sqla
from ..models import User
from .forms import LoginForm

# Create customized model view class
class UserRoleAdminView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('ROLE_USER_ADMIN'):
            return True

        return False


class IndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(IndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(IndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))
