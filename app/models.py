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
    active = db.Column(db.Boolean(), default=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    git_groups = db.relationship('GitGroup', backref='owner', lazy='dynamic')
    git_repos = db.relationship('GitRepo', backref='owner', lazy='dynamic')
    create_tickets = db.relationship('Ticket', backref='owner', lazy='dynamic', foreign_keys='Ticket.owner_id')
    approve_tickets = db.relationship('Ticket', backref='approve', lazy='dynamic', foreign_keys='Ticket.approve_id')
    repo_accesses = db.relationship('RepoAccess', backref='user', lazy='dynamic')
    group_accesses = db.relationship('GroupAccess', backref='user', lazy='dynamic')

    def __str__(self):
        return self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.name


class GitGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    git_id = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    git_repos = db.relationship('GitRepo', backref='group', lazy='dynamic')
    group_accesses = db.relationship('GroupAccess', backref='group', lazy='dynamic')

    def __str__(self):
        return self.name
    
    def to_string(self):
        return "Name: %s, Git Id: %s, Description: %s" % (self.name, self.git_id, self.description)

        
class GitRepo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('git_group.id'),
        nullable=False)
    repo_accesses = db.relationship('RepoAccess', backref='repo', lazy='dynamic')

    def __str__(self):
        return self.name
    
    def to_string(self):
        return "Name: %s, Group: %s, Description: %s" % (self.name, self.group, self.description)

class AccessType(Enum):
    ReadOnly = 'ReadOnly'
    ReadWrite = 'ReadWrite'

class RepoAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    repo_id = db.Column(db.Integer, db.ForeignKey('git_repo.id'),
        nullable=False)
    access_type = db.Column(db.Enum(AccessType), nullable=False)

    def __str__(self):
        return "User: %s, Repo: %s, Access: %s" % (self.user.name, self.repo, self.access_type)
    
    def to_string(self):
        return "User: %s, Repo: %s, Access: %s" % (self.user.name, self.repo, self.access_type)

class GroupAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('git_group.id'),
        nullable=False)
    access_type = db.Column(db.Enum(AccessType), nullable=False)

    def __str__(self):
        return "User: %s, Group: %s, Access: %s" % (self.user.name, self.group, self.access_type)
    
    def to_string(self):
        return "User: %s, Group: %s, Access: %s" % (self.user.name, self.group, self.access_type)

class TicketType(Enum):
    NewGroup = 'NewGroup'
    NewRepo = 'NewRepo'
    GroupAccess = 'GroupAccess'
    RepoAccess = 'RepoAccess'

class TicketStatus(Enum):
    Pending = 'Pending'
    Submit = 'Submit'
    Approve = 'Approve'
    Reject = 'Reject'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(TicketType))
    status = db.Column(db.Enum(TicketStatus))
    content = db.Column(db.Text)
    create_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)
    case_id = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    approve_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=True)
    

    def __str__(self):
        return self.content


 
