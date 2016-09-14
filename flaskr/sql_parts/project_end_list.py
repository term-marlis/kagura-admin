from sqlalchemy.sql import select
from sqlalchemy import func, and_, or_, text
from flaskr.sql_parts.abstract_parts import AbstractParts

class ProjectEndList(AbstractParts):

    def __init__(self, engine_):
        super().__init__(engine_)


    def columns(self):
        columns = [self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_memo_status,
            self.pt.c.project_target_status,
            self.pt.c.project_target_amount,
            self.pt.c.project_start_datetime,
            self.pt.c.project_end_datetime,
            func.sum(self.ust.c.user_support_amount).label('user_support_amount')
            ]
        return columns


    def outerjoin(self):
        return self.pt.outerjoin(
            self.ust,
            and_(
                self.ust.c.project_id==self.pt.c.project_id
            )
        )


    def where(self, form):
        self.query = self.query.where(self.pt.c.project_is_delete==0)
        self.query = self.query.where(self.pt.c.project_is_approval==1)
        self.query = self.query.where(text('pt.project_end_datetime <= now()'))

        request_form = form.to_dict()
        if request_form:
            print(request_form)
            for key in request_form.keys():
                if key.count('project_end_datime'):
                    key = str('project_end_datime')
                eval('self.where_' + str(key) + '(form)')


    def where_project_id(self, form):
        if 'project_id' in form and form['project_id']:
            self.query = self.query.where(self.pt.c.project_id==form['project_id'])


    def where_project_title(self, form):
        if 'project_title' in form and form['project_title']:
            self.query = self.query.where(self.pt.c.project_title==form['project_title'])


    def where_project_end_datime(self, form):
        if 'project_end_datetime_min' in form and form['project_end_datetime_min']:
            self.query = self.query.where(self.pt.c.project_end_datetime >= form['project_end_datetime_min'])
        if 'project_end_datetime_max' in form and form['project_end_datetime_max']:
            self.query = self.query.where(self.pt.c.project_end_datetime < form['project_end_datetime_max'])


    def where_project_memo_status(self, form):
        if 'project_memo_status' in form and form['project_memo_status']:
            self.query = self.query.where(pt.c.project_memo_status==form['project_memo_status'])


    def group_by(self):
        self.query = self.query.group_by(self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_memo_status,
            self.pt.c.project_target_status,
            self.pt.c.project_target_amount,
            self.pt.c.project_start_datetime,
            self.pt.c.project_end_datetime
            )
