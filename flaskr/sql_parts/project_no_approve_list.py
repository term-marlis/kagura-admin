from sqlalchemy.sql import select
from sqlalchemy import func, and_, or_, text
from flaskr.sql_parts.abstract_parts import AbstractParts

class ProjectNoApproveList(AbstractParts):

    def __init__(self, engine_):
        super().__init__(engine_)


    def columns(self):
        columns = [self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_start_datetime,
            self.pt.c.project_end_datetime,
            self.pt.c.project_reg_datetime
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
        self.query = self.query.where(self.pt.c.project_is_approval==0)
        
        request_form = form.to_dict()
        if request_form:
            print(request_form)
            for key in request_form.keys():
                if key.count('project_reg_datetime'):
                    key = str('project_reg_datetime')
                eval('self.where_' + str(key) + '(form)')


    def where_project_keyword(self, form):
        if 'project_keyword' in form and form['project_keyword']:
            keyword = str('%' + form['project_keyword'] + '%')
            self.query = self.query.where(or_(self.pt.c.project_title.like(keyword), self.pt.c.project_detail.like(keyword), self.pt.c.project_summary.like(keyword)))


    def where_project_reg_datetime(self, form):
        if 'project_reg_datetime_min' in form and form['project_reg_datetime_min']:
            self.query = self.query.where(self.pt.c.project_reg_datetime >= form['project_reg_datetime_min'])
        if 'project_reg_datetime_max' in form and form['project_reg_datetime_max']:
            self.query = self.query.where(self.pt.c.project_reg_datetime < form['project_reg_datetime_max'])


    def group_by(self):
        self.query = self.query.group_by(self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_start_datetime,
            self.pt.c.project_end_datetime,
            self.pt.c.project_reg_datetime)
