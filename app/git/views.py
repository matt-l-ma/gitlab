from flask import render_template, redirect, url_for,request, flash, session, jsonify
from flask_security import login_user, login_required, current_user, logout_user
from flask_admin import helpers, expose
from flask_admin.contrib import sqla
from flask_admin.form.fields import Select2Field
from ..models import TicketType, TicketStatus
from flask_admin.form import rules
from sqlalchemy import func
import time



class EnumSelect2Field(Select2Field):
    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == self.coerce(v):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class GitGroupView(sqla.ModelView):

    column_labels = dict(user='Owner')

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('ROLE_GIT_ADMIN'):
            return True

        return False


class GitRepoView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('ROLE_GIT_ADMIN'):
            return True

        return False


class MyTicketView(sqla.ModelView):

    column_exclude_list = ['approve_id']
    list_template = 'git/my_ticket_list.html'
    
    form_excluded_columns = ('status', 'user', 'approve_id', 'create_date', 'update_date')
    
    form_extra_fields = {
        'type': EnumSelect2Field(
            choices=[(x.name, x.name.title()) for x in TicketType],
            coerce=TicketType,
            default=TicketType['Group'])}
    
    form_rules = [
        rules.Field('type'),
        rules.Field('content')
    ]
    
    def is_action_allowed(self, name):
        return False
    
    def create_model(self, form):
        try:
            model = self.model()
            form.populate_obj(model)
            
            # prefill fields
            model.status = TicketStatus.Pending
            model.owner_id = current_user.id
            model.create_date = time.strftime('%Y-%m-%d %H:%M:%S')
            model.update_date = time.strftime('%Y-%m-%d %H:%M:%S')
            
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model

    def update_model(self, form, model):

        try:
            form.populate_obj(model)
            
            # fill update_time
            model.update_date = time.strftime('%Y-%m-%d %H:%M:%S')
            
            self._on_model_change(form, model, False)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to update record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to update record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, False)

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
        return self.session.query(func.count('*')).select_from(self.model).filter(self.model.owner_id == current_user.id)

    def is_pending(self, model):
        status = getattr(model, 'status')
        return status == TicketStatus.Pending
    
    @expose('/submit', methods=['POST'])
    def submit(self):
        self.session.query(self.model).filter(self.model.id == request.form['id']).update({self.model.status:'Submit'})
        self.session.commit()
        flash('Your request has been sent for approval')
        return redirect(url_for('.index_view'))



class TicketApproveView(sqla.ModelView):

    can_create = False
    can_edit = False
    can_delete = False
    
    list_template = 'git/ticket_approve_list.html'

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('ROLE_APPROVE'):
            return True
        return False

    def get_query(self):
        return self.session.query(self.model).filter(self.model.status == TicketStatus.Submit)
    
    def get_count_query(self):
        return self.session.query(func.count('*')).select_from(self.model).filter(self.model.status == TicketStatus.Submit)

    def is_submit(self, model):
        status = getattr(model, 'status')
        return status == TicketStatus.Submit
    
    @expose('/approve', methods=['POST'])
    def approve(self):
        self.session.query(self.model).filter(self.model.id == request.form['id']).update({self.model.status:'Approve', self.model.approve_id: current_user.id})
        self.session.commit()
        flash('Ticket id[%s] approved' % request.form['id'])
        return redirect(url_for('approval.index_view'))
        
    @expose('/reject', methods=['POST'])
    def reject(self):
        self.session.query(self.model).filter(self.model.id == request.form['id']).update({self.model.status:'Reject', self.model.approve_id: current_user.id})
        self.session.commit()
        flash('Ticket id[%s] rejected' % request.form['id'])
        return redirect(url_for('approval.index_view'))






