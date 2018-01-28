# -*- coding:utf-8 -*-

from flask_admin import helpers, Admin
from flask import Flask, url_for

from flask_security import Security, SQLAlchemyUserDatastore
from app import create_app, db
from app.models import User, Role, GitGroup, GitRepo, GroupAccess, RepoAccess, Ticket
from app.auth.views import UserAdminView, RoleAdminView, IndexView
from app.git.views import GitGroupView, GitRepoView, RepoAccessView, GroupAccessView, TicketView, TicketApproveView
from flask_admin.babel import gettext


app = create_app('default')
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Add model views
admin = Admin(app, u'配置管理系统', index_view=IndexView(), base_template='base.html')
admin.add_view(UserAdminView(User, db.session, name=u'用户', category=u'用户管理'))
admin.add_view(RoleAdminView(Role, db.session, name=u'角色', category=u'用户管理'))
admin.add_view(GitGroupView(GitGroup, db.session, name=u'Git组', category=gettext('Git管理')))
admin.add_view(GitRepoView(GitRepo, db.session, name=u'Git库', category=gettext('Git管理')))
admin.add_view(GroupAccessView(GroupAccess, db.session, name=u'组权限', category=gettext('Git管理')))
admin.add_view(RepoAccessView(RepoAccess, db.session, name=u'库权限', category=gettext('Git管理')))
admin.add_view(TicketView(Ticket, db.session, name=u'我的申请', category=u'申请列表', endpoint='ticket'))
admin.add_view(TicketApproveView(Ticket, db.session, name=u'我的审批', category=u'申请列表', endpoint='approval'))

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


