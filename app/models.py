from . import db
from . import login_manager
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from enum import Enum


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    git_groups = db.relationship('GitGroup', backref='user', lazy=True)
    tickets = db.relationship('Ticket', backref='user', lazy=True)

    def __str__(self):
        return self.email

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


class GitGroup(db.Model):
    __tablename__ = 'git_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    git_id = db.Column(db.String(255))
    description = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    git_repos = db.relationship('GitRepo', backref='git_group', lazy=True)

    def __str__(self):
        return self.name

        
class GitRepo(db.Model):
    __tablename__ = 'git_repo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey('git_group.id'),
        nullable=False)

    def __str__(self):
        return self.name


class TicketType(Enum):
    Group = 'Group'
    Repo = 'Repo'

class TicketStatus(Enum):
    Pending = 'Pending'
    Submit = 'Submit'
    Approve = 'Approve'
    Reject = 'Reject'

class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(TicketType))
    status = db.Column(db.Enum(TicketStatus))
    content = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    approve_id = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)

    def __str__(self):
        return self.content


 
