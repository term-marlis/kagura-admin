from sqlalchemy.sql import select
from sqlalchemy import func, and_, or_, text
from flaskr.sql_parts.abstract_parts import AbstractParts

class ProjectList(AbstractParts):

    def __init__(self, engine_):
        super().__init__(engine_)


    def columns(self):
        columns = [self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_public_status,
            self.pt.c.project_target_status,
            self.pt.c.project_is_approval,
            self.pt.c.project_is_pickup,
            self.pt.c.project_target_amount,
            self.pt.c.project_popular_order,
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
        self.query = self.query.where(self.pt.c.project_public_status==2)

        request_form = form.to_dict()
        if request_form:
            print(request_form)
            for key in request_form.keys():
                if key == 'list_type':
                    continue
                eval('self.where_' + str(key) + '(form)')


    def where_project_id(self, form):
        if 'project_id' in form and form['project_id']:
            self.query = self.query.where(self.pt.c.project_id==form['project_id'])


    def where_project_is_pickup(self, form):
        if 'project_is_pickup' in form:
            self.query = self.query.where(self.pt.c.project_is_pickup==1)


    def where_project_popular_order(self, form):
        if 'project_popular_order' in form:
            self.query = self.query.where(self.pt.c.project_popular_order>0)


    def where_project_type(self, form):
        if 'project_type' in form and form['project_type']:
            self.query = self.query.where(self.pt.c.project_type==form['project_type'])


    def where_project_keyword(self, form):
        if 'project_keyword' in form and form['project_keyword']:
            keyword = str('%' + form['project_keyword'] + '%')
            self.query = self.query.where(or_(self.pt.c.project_title.like(keyword), self.pt.c.project_detail.like(keyword), self.pt.c.project_summary.like(keyword)))


    def where_project_public_status(self, form):
        if 'project_public_status' in form and form['project_public_status']:
            self.query = self.query.where(self.pt.c.project_public_status==form['project_public_status'])


    def where_project_target_status(self, form):
        if 'project_target_status' in form and form['project_target_status']:
            if form['project_target_status'] == '1' or form['project_target_status'] == '2':
                self.query = self.query.where(text('pt.project_end_datetime < now()'))

            if form['project_target_status'] == '3' or form['project_target_status'] == '4':
                self.query = self.query.where(text('pt.project_end_datetime >= now()'))

            if form['project_target_status'] == '1' or form['project_target_status'] == '4':
                self.query = self.query.having(text('(sum(ust.user_support_amount) < pt.project_target_amount or sum(ust.user_support_amount) is null)'))

            if form['project_target_status'] == '2' or form['project_target_status'] == '3':
                self.query = self.query.having(func.sum(self.ust.c.user_support_amount) >= self.pt.c.project_target_amount)


    def where_project_is_approval(self, form):
        if 'project_is_approval' in form and form['project_is_approval']:
            self.query = self.query.where(self.pt.c.project_is_approval==form['project_is_approval'])


    def group_by(self):
        self.query = self.query.group_by(self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_public_status,
            self.pt.c.project_target_status,
            self.pt.c.project_is_approval,
            self.pt.c.project_is_pickup,
            self.pt.c.project_target_amount,
            self.pt.c.project_popular_order,
            self.pt.c.project_start_datetime,
            self.pt.c.project_end_datetime
            )
