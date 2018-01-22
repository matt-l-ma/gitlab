#!/usr/bin/env python

from flask_admin import helpers, Admin
from flask import Flask, url_for
from flask_security import Security, SQLAlchemyUserDatastore
from app import create_app, db
from app.models import User, Role, GitGroup, GitRepo, Ticket
from app.auth.views import UserRoleAdminView, IndexView
from app.git.views import GitGroupView, GitRepoView, MyTicketView, TicketApproveView

app = create_app('default')
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Add model views
admin = Admin(app, 'GMS', index_view=IndexView(), base_template='base.html')
admin.add_view(UserRoleAdminView(User, db.session, name='User', category='User'))
admin.add_view(UserRoleAdminView(Role, db.session, name='Role', category='User'))
admin.add_view(GitGroupView(GitGroup, db.session, name='Group', category='Git'))
admin.add_view(GitRepoView(GitRepo, db.session, name='Repo', category='Git'))
admin.add_view(MyTicketView(Ticket, db.session, name='My Ticket', category='Ticket', endpoint='ticket'))
admin.add_view(TicketApproveView(Ticket, db.session, name='Approval', category='Ticket', endpoint='approval'))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template = admin.base_template,
        admin_view = admin.index_view,
        h = helpers,
        get_url = url_for
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')


