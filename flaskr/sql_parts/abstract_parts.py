# from flask import current_app
# from sqlalchemy.sql import select
# from sqlalchemy import Table, MetaData, func, and_, or_, text
# from sqlalchemy.orm import aliased

from abc import *
from sqlalchemy.sql import select
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import aliased

class AbstractParts(object):

    def __init__(self, engine_):
        self.engine = engine_
        metadata = MetaData(bind=engine_)
        project_table = Table('project', metadata, autoload=True)
        user_support_table = Table('user_support', metadata, autoload=True)
        self.pt = aliased(project_table, name='pt')
        self.ust = aliased(user_support_table, name='ust')
        self.query = None

    def select(self):
        self.query = select(self.columns())

    def from_table(self):
        self.query = self.query.select_from(self.outerjoin())

    @abstractmethod
    def columns():
        raise NotImplementedError()

    @abstractmethod
    def outerjoin():
        raise NotImplementedError()

    @abstractmethod
    def where(self, form):
        raise NotImplementedError()

    @abstractmethod
    def group_by(self):
        raise NotImplementedError()
