from flask import render_template, redirect, url_for,request, flash, session, jsonify
from flask_security import login_user, login_required, current_user, logout_user
from flask_admin import helpers, expose
from flask_admin.contrib import sqla
from flask_admin.form.fields import Select2Field
from ..models import TicketType, TicketStatus


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

    column_exclude_list = ['user', 'approve_id']
    list_template = 'git/my_ticket_list.html'
    
    form_extra_fields = {
        'type': EnumSelect2Field(
            choices=[(x.name, x.name.title()) for x in TicketType],
            coerce=TicketType,
            default=TicketType['Group'])}

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        return True

    def get_query(self):
        if current_user.has_role('ROLE_GIT_ADMIN'):
            return self.session.query(self.model).filter()
        else:
            return self.session.query(self.model).filter(self.model.owner_id == current_user.id)

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
        if current_user.has_role('ROLE_GIT_ADMIN'):
            return True
        return False

    def get_query(self):
        return self.session.query(self.model).filter(self.model.status == TicketStatus.Submit)

    def is_submit(self, model):
        status = getattr(model, 'status')
        return status == TicketStatus.Submit
    
    @expose('/approve', methods=['POST'])
    def approve(self):
        self.session.query(self.model).filter(self.model.id == request.form['id']).update({self.model.status:'Approve'})
        self.session.commit()
        flash('Ticket id[%s] approved' % request.form['id'])
        return redirect(url_for('approval.index_view'))
        
    @expose('/reject', methods=['POST'])
    def reject(self):
        self.session.query(self.model).filter(self.model.id == request.form['id']).update({self.model.status:'Reject'})
        self.session.commit()
        flash('Ticket id[%s] rejected' % request.form['id'])
        return redirect(url_for('approval.index_view'))






