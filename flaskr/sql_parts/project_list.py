from sqlalchemy.sql import select
from sqlalchemy import func, and_, or_, text
from flaskr.sql_parts.abstract_parts import AbstractParts
# engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')

class ProjectList(AbstractParts):

    def __init__(self, engine_):
        super().__init__(engine_)


    def columns(self):
        columns = [self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_public_status,
            self.pt.c.project_target_status,
            self.pt.c.project_is_approval,
            self.pt.c.project_target_amount,
            self.pt.c.project_popular_order,
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


    def where_project_id(self, form):
        if 'project_id' in form:
            self.query = self.query.where(pt.c.project_id==form['project_id'])


    def where_keyword(self, form):
        if 'keyword' in form and form['keyword']:
            keyword = str('%' + form['keyword'] + '%')
            self.query = self.query.where(or_(self.pt.c.project_title.like(keyword), self.pt.c.project_detail.like(keyword), self.pt.c.project_summary.like(keyword)))


    # def where_public_status(query, form):
    #     query = query.where(pt.c.project_public_status==2)
    #     query = query.where(pt.c.project_is_approval==1)
    #     return query


    def where_public_status(self, form):
        if 'project_public_status' in form:
            self.query = self.query.where(self.pt.c.project_public_status==form['project_public_status'])
            if form['project_public_status'] == 5:
                """削除の時はフラグも参照する"""
                self.query = self.query.where(pt.c.project_is_delete==1)


    def where_end_datetime(self, form):
        if 'project_target_status' in form:
            if form['project_target_status'] == 1 or form['project_target_status'] == 2:
                self.query = self.query.where(text('pt.project_end_datetime < now()'))
            if form['project_target_status'] == 3:
                self.query = self.query.where(text('pt.project_end_datetime >= now()'))


    def where_project_memo_status(self, form):
        if 'project_memo_status' in form and form['project_memo_status']:
            self.query = self.query.where(pt.c.project_memo_status==form['project_memo_status'])


    def group_by(self):
        self.query = self.query.group_by(self.pt.c.project_id,
            self.pt.c.project_title,
            self.pt.c.project_public_status,
            self.pt.c.project_target_status,
            self.pt.c.project_is_approval,
            self.pt.c.project_target_amount,
            self.pt.c.project_popular_order)


    def having_target_status(self, form):
        if 'project_target_status' in form and form['project_target_status']:
            if form['project_target_status'] == '1':
                self.query = self.query.having(or_(func.sum(self.ust.c.user_support_amount) < self.pt.c.project_target_amount, func.sum(self.ust.c.user_support_amount) is None))
            if form['project_target_status'] == '2':
                self.query = self.query.having(func.sum(self.ust.c.user_support_amount) >= self.pt.c.project_target_amount)
