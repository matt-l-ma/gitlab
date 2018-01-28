# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for,request, flash, session, jsonify
from flask_security import login_user, login_required, current_user, logout_user
from flask_admin import helpers, expose
from flask_admin.contrib import sqla
from flask_admin.form.fields import Select2Field
from ..models import User, GitRepo, GitGroup, RepoAccess, GroupAccess, TicketType, TicketStatus
from flask_admin.form import rules
from sqlalchemy import func, literal

import time
from flask_admin.helpers import (get_form_data, validate_form_on_submit,
                                 get_redirect_target, flash_errors)
from flask_admin.contrib.sqla.form import get_form
from pprint import pprint
from flask_admin.babel import gettext
from wtforms.validators import AnyOf
from pprint import pprint



class GitGroupView(sqla.ModelView):
    def is_accessible(self):
        self.can_create = current_user.has_role('ROLE_GIT_ADMIN')
        self.can_edit = current_user.has_role('ROLE_GIT_ADMIN')
        self.can_delete = current_user.has_role('ROLE_GIT_ADMIN')
        
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.git_groups.count() != 0:
            return True
        if current_user.has_role('ROLE_GIT_ADMIN'):
            return True
        return False


class GitRepoView(sqla.ModelView):
    def is_accessible(self):
        self.can_create = current_user.has_role('ROLE_GIT_ADMIN')
        self.can_edit = current_user.has_role('ROLE_GIT_ADMIN')
        self.can_delete = current_user.has_role('ROLE_GIT_ADMIN')
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.git_repos.count() != 0:
            return True
        if current_user.has_role('ROLE_GIT_ADMIN'):
            return True
        return False

class RepoAccessView(sqla.ModelView):
    def is_accessible(self):
        self.can_create = current_user.has_role('ROLE_GIT_ADMIN')
        self.can_edit = current_user.has_role('ROLE_GIT_ADMIN')
        self.can_delete = current_user.has_role('ROLE_GIT_ADMIN')
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.repo_accesses.count() != 0:
            return True
        if current_user.has_role('ROLE_GIT_ADMIN'):
            return True
        return False
        
class GroupAccessView(sqla.ModelView):
    def is_accessible(self):
        self.can_create = current_user.has_role('ROLE_GIT_ADMIN')
        self.can_edit = current_user.has_role('ROLE_GIT_ADMIN')
        self.can_delete = current_user.has_role('ROLE_GIT_ADMIN')
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.group_accesses.count() != 0:
            return True
        if current_user.has_role('ROLE_GIT_ADMIN'):
            return True
        return False

def column_converter_type(v, c, m, p):
    if m.type == TicketType.NewRepo:
        return u'新建库'
    elif m.type == TicketType.NewGroup:
        return u'新建组'
    elif m.type == TicketType.RepoAccess:
        return u'库权限'
    elif m.type == TicketType.GroupAccess:
        return u'组权限'

def column_converter_status(v, c, m, p):
    if m.status == TicketStatus.Pending:
        return u'未提交'
    elif m.status == TicketStatus.Submit:
        return u'已提交'
    elif m.status == TicketStatus.Approve:
        return u'批准'
    elif m.status == TicketStatus.Reject:
        return u'驳回'

class TicketView(sqla.ModelView):

    can_edit = False
    column_exclude_list = ['approve_id', 'case_id']
    list_template = 'git/ticket_list.html'
    create_template = 'git/ticket_create.html'
    edit_template = 'git/ticket_edit.html'
    
    column_labels = dict(
        type=u'类型',
        status=u'状态',
        content=u'描述',
        create_date=u'创建时间',
        update_date=u'更新时间',
        owner=u'创建者',
        approve=u'审核者')
    
    column_formatters = dict(
        type = column_converter_type,
        status = column_converter_status
    )
    
    def is_action_allowed(self, name):
        return False
    
    def create_model(self, form, model_class, ticket_type):
        try:
            content_model = model_class()
            form.populate_obj(content_model)
            self.session.add(content_model)
            self.session.commit()
            
            # prefill fields
            ticket = self.model()
            ticket.status = TicketStatus.Pending
            ticket.type = ticket_type
            ticket.owner_id = current_user.id
            ticket.create_date = time.strftime('%Y-%m-%d %H:%M:%S')
            ticket.update_date = time.strftime('%Y-%m-%d %H:%M:%S')
            ticket.content = content_model.to_string()
            ticket.case_id = content_model.id
            
            self.session.add(ticket)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(u'创建记录失败.', 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False

        return ticket
    
    def delete_model(self, model):
        try:
            self.session.flush()
            self.session.delete(model)
            
            # delete the inactive case
            if model.type == TicketType.NewRepo:
                self.session.query(GitRepo).filter(GitRepo.id == model.case_id).delete()
            elif model.type == TicketType.NewGroup:
                self.session.query(GitGroup).filter(GitGroup.id == model.case_id).delete()
            elif model.type == TicketType.RepoAccess:
                self.session.query(RepoAccess).filter(RepoAccess.id == model.case_id).delete()
            elif model.type == TicketType.GroupAccess:
                self.session.query(GroupAccess).filter(GroupAccess.id == model.case_id).delete()
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(u'删除记录失败.', 'error')
                log.exception('Failed to delete record.')
            self.session.rollback()
            return False

        return True
        
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        return True

    def get_query(self):
        if current_user.has_role('ROLE_GIT_ADMIN'):
            return self.session.query(self.model).filter()
        else:
            return self.session.query(self.model).filter(self.model.owner_id == current_user.id)
    
    def get_count_query(self):
        if current_user.has_role('ROLE_GIT_ADMIN'):
            return self.session.query(func.count('*')).select_from(self.model).filter()
        else:
            return self.session.query(func.count('*')).select_from(self.model).filter(self.model.owner_id == current_user.id)

    def is_pending(self, model):
        status = getattr(model, 'status')
        return status == TicketStatus.Pending
    
    def create_form_view(self, view_model, ticket_type, form_view):
        return_url = get_redirect_target() or self.get_url('.index_view')
        converter = self.model_form_converter(self.session, form_view)
        form = get_form(view_model, converter,
                        base_class=form_view.form_base_class,
                        only=form_view.form_columns,
                        exclude=form_view.form_excluded_columns,
                        field_args=form_view.form_args,
                        ignore_hidden=form_view.ignore_hidden,
                        extra_fields=form_view.form_extra_fields)(get_form_data())
        
        if self.validate_form(form):
            model = self.create_model(form, view_model, ticket_type)
            if model:
                flash(u'新建记录成功.', 'success')
                return redirect(self.get_save_return_url(model, is_created=True))
        
        return self.render(self.create_template,
                        form=form,
                        count=self.get_count_query().first()[0],
                        active_tab=ticket_type.value,
                        return_url=return_url
                        )
        
    @expose('/apply_new_repo/', methods=('GET', 'POST'))
    def apply_new_repo_view(self):
        form_view = sqla.ModelView(GitRepo, self.session)
        form_view.form_columns = ('name', 'group', 'description', 'owner')
        form_view.form_args = {
            'name': {
                'label': u'库名'
            },
            'group': {
                'label': u'所属组',
                'query_factory': lambda: self.session.query(GitGroup).filter_by(active=True)
            },
            'description':{
                'label': u'描述'
            },
            'owner': {
                'label': u'申请者',
                'query_factory': lambda: self.session.query(User).filter_by(id=current_user.id)
            }
        }
        return self.create_form_view(GitRepo, TicketType.NewRepo, form_view)
        
    @expose('/apply_new_group/', methods=('GET', 'POST'))
    def apply_new_group_view(self):
        form_view = sqla.ModelView(GitGroup, self.session)
        form_view.form_columns = ('name', 'git_id', 'description', 'owner')
        form_view.form_args = {
            'name': {
                'label': u'组名'
            },
            'description':{
                'label': u'描述'
            },
            'owner': {
                'label': u'申请者',
                'query_factory': lambda: self.session.query(User).filter_by(id=current_user.id)
            }
        }
        return self.create_form_view(GitGroup, TicketType.NewGroup, form_view)
        
    @expose('/apply_repo_access/', methods=('GET', 'POST'))
    def apply_repo_access_view(self):
        form_view = sqla.ModelView(RepoAccess, self.session)
        form_view.form_columns = ('repo', 'access_type', 'user')
        form_view.form_args = {
            'repo': {
                'label': u'库',
                'query_factory': lambda: self.session.query(GitRepo).filter_by(active=True)
            },
            'access_type': { 'label' : u'权限' },
            'user': {
                'label': u'申请者',
                'query_factory': lambda: self.session.query(User).filter_by(id=current_user.id)
            }
        }
        return self.create_form_view(RepoAccess, TicketType.RepoAccess, form_view)
        
    @expose('/apply_group_access/', methods=('GET', 'POST'))
    def apply_group_access_view(self):
        form_view = sqla.ModelView(GroupAccess, self.session)
        form_view.form_columns = ('group', 'access_type', 'user')
        form_view.form_args = {
            'group': {
                'label': u'组',
                'query_factory': lambda: self.session.query(GitGroup).filter_by(active=True)
            },
            'access_type': { 'label' : u'权限' },
            'user': {
                'label': u'申请者',
                'query_factory': lambda: self.session.query(User).filter_by(id=current_user.id)
            }
        }
        return self.create_form_view(GroupAccess, TicketType.GroupAccess, form_view)
    
    @expose('/submit', methods=['POST'])
    def submit(self):
        self.session.query(self.model).filter(self.model.id == request.form['id']) \
            .update({
                self.model.status:'Submit',
                self.model.update_date:time.strftime('%Y-%m-%d %H:%M:%S')})
        self.session.commit()
        flash(u'你的申请已经提交审批.', 'success')
        return redirect(url_for('.index_view'))



class TicketApproveView(sqla.ModelView):

    can_create = False
    can_edit = False
    can_delete = False
    
    column_exclude_list = ['approve', 'status', 'update_date', 'case_id']
    column_display_actions = False
    column_labels = dict(
        type=u'类型',
        content=u'描述',
        create_date=u'创建时间',
        owner=u'创建者')
    
    list_template = 'git/ticket_approve_list.html'

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        
        # owner for any repo/group have access
        if current_user.git_groups.filter(GitGroup.active==True).count() != 0 \
            or current_user.git_repos.filter(GitRepo.active==True).count() != 0:
            return True
        
        # super account
        if current_user.has_role('ROLE_APPROVE'):
            return True
        return False

    def get_query(self):
        if current_user.has_role('ROLE_GIT_ADMIN'):
            return self.session.query(self.model).filter(self.model.status == TicketStatus.Submit)
        else:
            q_new_repo = self.session.query(self.model)\
                            .filter(self.model.status == TicketStatus.Submit, self.model.type == TicketType.NewRepo)\
                            .join(GitRepo, self.model.case_id == GitRepo.id)\
                            .join(GitGroup, GitRepo.group_id == GitGroup.id)\
                            .join(User, GitGroup.owner_id == User.id)\
                            .filter(User.id == current_user.id)
            q_repo_access = self.session.query(self.model)\
                            .filter(self.model.status == TicketStatus.Submit, self.model.type == TicketType.RepoAccess)\
                            .join(RepoAccess, self.model.case_id == RepoAccess.id)\
                            .join(GitRepo, RepoAccess.repo_id == GitRepo.id)\
                            .join(User, GitRepo.owner_id == User.id)\
                            .filter(User.id == current_user.id)
            q_group_access = self.session.query(self.model)\
                            .filter(self.model.status == TicketStatus.Submit, self.model.type == TicketType.GroupAccess)\
                            .join(GroupAccess, self.model.case_id == GroupAccess.id)\
                            .join(GitGroup, GroupAccess.group_id == GitGroup.id)\
                            .join(User, GitGroup.owner_id == User.id)\
                            .filter(User.id == current_user.id) 
            return q_new_repo.union(q_repo_access).union(q_group_access)
    def get_count_query(self):
        return self.session.query(literal(self.get_query().count()))

    def is_submit(self, model):
        status = getattr(model, 'status')
        return status == TicketStatus.Submit
    
    @expose('/approve', methods=['POST'])
    def approve(self):
        try:
            ticket = self.session.query(self.model).filter(self.model.id == request.form['id']).first()
            ticket.status = TicketStatus.Approve
            ticket.approve_id = current_user.id

            # make the case active
            if ticket.type == TicketType.NewRepo:
                self.session.query(GitRepo).filter(GitRepo.id == ticket.case_id).update({'active':True})
            elif ticket.type == TicketType.NewGroup:
                self.session.query(GitGroup).filter(GitGroup.id == ticket.case_id).update({'active':True})
            elif ticket.type == TicketType.RepoAccess:
                self.session.query(RepoAccess).filter(RepoAccess.id == ticket.case_id).update({'active':True})
            elif ticket.type == TicketType.GroupAccess:
                self.session.query(GroupAccess).filter(GroupAccess.id == ticket.case_id).update({'active':True})
            self.session.commit()
            flash(u'申请 id[%s] 已经批准.' % request.form['id'], 'success')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(u'变形失败.', 'error')
                log.exception('Failed to change status.')
            self.session.rollback()
        
        return redirect(url_for('approval.index_view'))
        
    @expose('/reject', methods=['POST'])
    def reject(self):
        try:
            ticket = self.session.query(self.model).filter(self.model.id == request.form['id']).first()
            ticket.status = TicketStatus.Reject
            ticket.approve_id = current_user.id

            # delete the inactive case
            if ticket.type == TicketType.NewRepo:
                self.session.query(GitRepo).filter(GitRepo.id == ticket.case_id).delete()
            elif ticket.type == TicketType.NewGroup:
                self.session.query(GitGroup).filter(GitGroup.id == ticket.case_id).delete()
            elif ticket.type == TicketType.RepoAccess:
                self.session.query(RepoAccess).filter(RepoAccess.id == ticket.case_id).delete()
            elif ticket.type == TicketType.GroupAccess:
                self.session.query(GroupAccess).filter(GroupAccess.id == ticket.case_id).delete()

            self.session.commit()
            flash(u'申请 id[%s] 已驳回' % request.form['id'], 'success')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(u'变形失败.', 'error')
                log.exception('Failed to change status.')
            self.session.rollback()
        
        return redirect(url_for('approval.index_view'))
        





