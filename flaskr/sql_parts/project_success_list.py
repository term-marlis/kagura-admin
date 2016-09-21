from sqlalchemy.sql import select
from sqlalchemy import func, and_, or_, text
from flaskr.sql_parts.abstract_parts import AbstractParts

class ProjectSuccessList(AbstractParts):

    def __init__(self, engine_):
        super().__init__(engine_)

    def columns(self):
        columns = [self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_public_status,
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
        self.query = self.query.where(text('pt.project_end_datetime > now()'))
        self.query = self.query.where(text('pt.project_start_datetime <= now()'))
        self.query = self.query.having(func.sum(self.ust.c.user_support_amount) >= self.pt.c.project_target_amount)

        request_form = form.to_dict()
        if request_form:
            print(request_form)
            for key in request_form.keys():
                if key == 'list_type':
                    continue
                if key.count('project_start_datetime'):
                    key = str('project_start_datetime')
                eval('self.where_' + str(key) + '(form)')

    def where_project_id(self, form):
        if 'project_id' in form and form['project_id']:
            self.query = self.query.where(self.pt.c.project_id==form['project_id'])

    def where_project_type(self, form):
        if 'project_type' in form and form['project_type']:
            self.query = self.query.where(self.pt.c.project_type==form['project_type'])

    def where_project_start_datetime(self, form):
        if 'project_start_datetime_min' in form and form['project_start_datetime_min']:
            self.query = self.query.where(self.pt.c.project_end_datetime >= form['project_start_datetime_min'])
        if 'project_start_datetime_max' in form and form['project_start_datetime_max']:
            self.query = self.query.where(self.pt.c.project_end_datetime < form['project_start_datetime_max'])

    def where_project_public_status(self, form):
        if 'project_public_status' in form and form['project_public_status']:
            self.query = self.query.where(self.pt.c.project_public_status==form['project_public_status'])

    def where_project_keyword(self, form):
        if 'project_keyword' in form and form['project_keyword']:
            keyword = str('%' + form['project_keyword'] + '%')
            self.query = self.query.where(or_(self.pt.c.project_title.like(keyword), self.pt.c.project_detail.like(keyword), self.pt.c.project_summary.like(keyword)))

    def group_by(self):
        self.query = self.query.group_by(self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_public_status,
            self.pt.c.project_target_amount,
            self.pt.c.project_start_datetime,
            self.pt.c.project_end_datetime
            )
