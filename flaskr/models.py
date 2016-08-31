from sqlalchemy.orm import synonym
from werkzeug import check_password_hash, generate_password_hash

from flaskr import db

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT, INTEGER
from sqlalchemy import Table, MetaData, func, and_
from flask import current_app
from sqlalchemy.sql import select


# class User(db.Model):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), default='', nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     _password = db.Column('password', db.String(100), nullable=False)
#
#     def _get_password(self):
#         return self._password
#     def _set_password(self, password):
#         if password:
#             password = password.strip()
#         self._password = generate_password_hash(password)
#     password_descriptor = property(_get_password, _set_password)
#     password = synonym('_password', descriptor=password_descriptor)
#
#     def check_password(self, password):
#         password = password.strip()
#         if not password:
#             return False
#         return check_password_hash(self.password, password)
#
#     @classmethod
#     def authenticate(cls, query, email, password):
#         user = query(cls).filter(cls.email==email).first()
#         if user is None:
#             return None, False
#         return user, user.check_password(password)
#
#     def __repr__(self):
#         return u'<User id={self.id} email={self.email!r}>'.format(
#                 self=self)


class Admin(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('admin_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    role = db.Column('admin_role', db.Integer, nullable=False, default=1)
    name = db.Column('admin_name', db.VARCHAR(255, collation='utf8_unicode_ci'))
    login_email = db.Column('admin_login_email', db.VARCHAR(255, collation='utf8_unicode_ci'))
    login_pw = db.Column('admin_login_pw', db.VARCHAR(255, collation='utf8_unicode_ci'))
    download_permission = db.Column('admin_download_permission', db.Integer, nullable=False, default=0)
    is_delete = db.Column('admin_is_delete', TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column('admin_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('admin_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class Bank(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('bank_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    project_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.VARCHAR(255), nullable=False)
    user_email = db.Column(db.VARCHAR(255), nullable=False)
    user_phone_number = db.Column(db.VARCHAR(255), nullable=False)
    name = db.Column('bank_name', db.VARCHAR(255), nullable=False)
    code = db.Column('bank_code', db.VARCHAR(255), nullable=True, default=None)
    branch_name = db.Column('bank_branch_name', db.VARCHAR(255), nullable=False)
    branch_code = db.Column('bank_branch_code', db.VARCHAR(255), nullable=True, default=None)
    account_type = db.Column('bank_account_type', TINYINT(1), nullable=False, default=1)
    account_number = db.Column('bank_account_number', db.VARCHAR(255), nullable=False)
    account_name_kana = db.Column('bank_account_name_kana', db.VARCHAR(255), nullable=False)
    reg_datetime = db.Column('bank_account_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('bank_account_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class CronLog(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('cron_log_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    project_id = db.Column('cron_log_project_id', db.Integer, nullable=False)
    credit_id = db.Column('cron_log_credit_id', db.Integer, nullable=False)
    credit_status = db.Column('cron_log_credit_status', db.VARCHAR(50), nullable=False)
    support_content = db.Column('cron_log_support_content', db.TEXT, nullable=False)
    reg_datetime = db.Column('cron_log_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('cron_log_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class GmoCredit(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('credit_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(INTEGER(unsigned=True), index=True, nullable=False)
    gmo_member_id = db.Column('user_gmo_member_id', db.VARCHAR(60, collation='utf8_unicode_ci'), nullable=False)
    status = db.Column('credit_status', db.Enum('未決済', '即時売上', '取消', '実売上', '仮売上'), nullable=False, default='未決済')
    error_code = db.Column('credit_error_code', db.VARCHAR(100, collation='utf8_unicode_ci'), default=None)
    check_string = db.Column('credit_check_string', db.VARCHAR(32, collation='utf8_unicode_ci'), default=None)
    access_id = db.Column('credit_access_id', db.VARCHAR(32, collation='utf8_unicode_ci'), default=None)
    access_pass = db.Column('credit_access_pass', db.VARCHAR(32, collation='utf8_unicode_ci'), default=None)
    forward = db.Column('credit_forward', db.VARCHAR(10, collation='utf8_unicode_ci'), default=None)
    approve = db.Column('credit_approve', db.VARCHAR(10, collation='utf8_unicode_ci'), default=None)
    order_id = db.Column('credit_order_id', db.VARCHAR(30, collation='utf8_unicode_ci'), default=None)
    tran_id = db.Column('credit_tran_id', db.VARCHAR(28, collation='utf8_unicode_ci'), default=None)
    tran_date = db.Column('credit_tran_date', db.VARCHAR(14, collation='utf8_unicode_ci'), default=None)
    convenience = db.Column('credit_convenience', db.VARCHAR(5, collation='utf8_unicode_ci'), default=None)
    receipt_no = db.Column('credit_receipt_no', db.VARCHAR(32, collation='utf8_unicode_ci'), default=None)
    conf_no = db.Column('credit_conf_no', db.VARCHAR(20, collation='utf8_unicode_ci'), default=None)
    encrypt_receipt_no = db.Column('credit_encrypt_receipt_no', db.VARCHAR(128, collation='utf8_unicode_ci'),
                                   default=None)
    bk_code = db.Column('credit_bk_code', db.VARCHAR(5, collation='utf8_unicode_ci'), default=None)
    cust_id = db.Column('credit_cust_id', db.VARCHAR(11, collation='utf8_unicode_ci'), default=None)
    payment_term = db.Column('credit_payment_term', db.VARCHAR(14, collation='utf8_unicode_ci'), default=None)
    reg_datetime = db.Column('gmo_credit_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('gmo_credit_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class PaymentHistory(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    gmo_credit_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    gmo_credit_mod_datetime = db.Column(db.DATETIME, primary_key=True)
    payment_datetime = db.Column(db.DATETIME, nullable=False)
    member_id = db.Column(db.VARCHAR(20), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    device = db.Column(db.VARCHAR(10), nullable=False, default='Others')
    project_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    payment_type = db.Column(db.Integer, nullable=False)
    changed_status = db.Column(TINYINT(1), nullable=False, default=0)
    amount = db.Column(db.Integer, nullable=False)
    reg_datetime = db.Column(db.DATETIME, default=datetime.now)


class GmoErrorLog(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('error_log_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    gmo_member_id = db.Column('user_gmo_member_id', db.VARCHAR(60), nullable=False)
    file = db.Column('error_log_file', db.VARCHAR(100), nullable=False)
    line = db.Column('error_log_line', db.Integer, nullable=False)
    message = db.Column('error_log_message', db.VARCHAR(100), nullable=False)
    param = db.Column('error_log_param', db.TEXT, nullable=False)
    reg_datetime = db.Column('error_log_reg_datetime', db.DATETIME, default=datetime.now)


class Information(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('information_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column('information_title', db.VARCHAR(255, collation='utf8_unicode_ci'), nullable=False)
    content = db.Column('information_content', db.TEXT(collation='utf8_unicode_ci'))
    type = db.Column('information_type', TINYINT(1), nullable=False)
    start_datetime = db.Column('information_start_datetime', db.DATETIME, default=None)
    end_datetime = db.Column('information_end_datetime', db.DATETIME, default=None)
    status = db.Column('information_status', TINYINT(1), nullable=False)
    pdf = db.Column('information_pdf', db.VARCHAR(255, collation='utf8_unicode_ci'), nullable=False)
    is_delete = db.Column('information_is_delete', TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column('information_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('information_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class Project(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('project_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column('project_title', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    image = db.Column('project_image', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    image_detail = db.Column('project_image_detail', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    image_detail_ = db.Column('project_image_detail_', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    type = db.Column('project_type', TINYINT(4), nullable=False, default=2)
    summary = db.Column('project_summary', db.TEXT(collation='utf8_unicode_ci'), default=None)
    period_type = db.Column('project_period_type', TINYINT(1), nullable=False, default=1)
    funding_days = db.Column('project_funding_days', TINYINT(1), nullable=False, default=0)
    start_datetime = db.Column('project_start_datetime', db.DATETIME, default=None)
    end_datetime = db.Column('project_end_datetime', db.DATETIME, default=None)
    place = db.Column('project_place', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    target_amount = db.Column('project_target_amount', db.Integer, default=0)
    open_amount = db.Column('project_open_amount', TINYINT(1), nullable=False, default=1)
    movie_code = db.Column('project_movie_code', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    detail = db.Column('project_detail', LONGTEXT(collation='utf8_unicode_ci'), default=None)
    note = db.Column('project_note', db.TEXT(collation='utf8_unicode_ci'), default=None)
    memo = db.Column('project_memo', db.TEXT(collation='utf8_unicode_ci'), default=None)
    approve_memo = db.Column('project_approve_memo', db.TEXT(collation='utf8_unicode_ci'), default=None)
    public_memo = db.Column('project_public_memo', db.TEXT(collation='utf8_unicode_ci'), default=None)
    delete_memo = db.Column('project_delete_memo', db.TEXT(collation='utf8_unicode_ci'), default=None)
    memo_status = db.Column('project_memo_status', TINYINT(1), nullable=False, default=1)
    is_approval = db.Column('project_is_approval', TINYINT(1), nullable=False, default=3)
    public_status = db.Column('project_public_status', TINYINT(1), nullable=False, default=1)
    target_status = db.Column('project_target_status', TINYINT(1), nullable=False, default=1)
    is_pickup = db.Column('project_is_pickup', TINYINT(1), nullable=False, default=0)
    is_cat_pickup = db.Column('project_is_cat_pickup', TINYINT(1), nullable=False, default=0)
    popular_order = db.Column('project_popular_order', TINYINT(1), nullable=False, default=0)
    main_color = db.Column('project_main_color', db.VARCHAR(25), default="#FFFFFF")
    accent_color = db.Column('project_accent_color', db.VARCHAR(25), default="#000000")
    is_delete = db.Column('project_is_delete', TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column('project_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('project_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class ProjectFaq(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('project_faq_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    project_id = db.Column(db.Integer, nullable=False)
    question = db.Column('project_faq_question', db.TEXT(collation='utf8_unicode_ci'), default=None)
    answer = db.Column('project_faq_answer', db.TEXT(collation='utf8_unicode_ci'), default=None)
    reg_datetime = db.Column('project_faq_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('project_faq_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class ProjectReport(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('project_report_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    name = db.Column('project_report_name', db.VARCHAR(255, collation='utf8_unicode_ci'), nullable=False)
    detail = db.Column('project_report_detail', LONGTEXT(collation='utf8_unicode_ci'), nullable=False)
    approval = db.Column('project_report_approval', TINYINT(1), nullable=False, default=0)
    accessible = db.Column('project_report_accessible', db.VARCHAR(20), nullable=False, default='all')
    reg_datetime = db.Column('project_report_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('project_report_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class ProjectItem(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('project_item_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    name = db.Column('project_item_name', db.VARCHAR(255, collation='utf8_unicode_ci'), nullable=False)
    image = db.Column('project_item_image', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    sequence = db.Column('project_item_sequence', db.Integer, nullable=False)
    money = db.Column('project_item_money', db.Integer, nullable=False, default=0)
    deliver_date = db.Column('project_item_deliver_date', db.DATE, nullable=False)
    detail = db.Column('project_item_detail', db.TEXT(collation='utf8_unicode_ci'), nullable=False)
    limit = db.Column('project_item_limit', db.Integer, default=None)
    limit_user = db.Column('project_item_limit_user', db.Integer, default=None)
    remain = db.Column('project_item_remain', db.Integer, nullable=False)
    type = db.Column('project_item_type', TINYINT(4), nullable=False, default=0)
    is_delete = db.Column('project_item_is_delete', TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column('project_item_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('project_item_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class ItemQuestion(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    project_item_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.VARCHAR(255, collation='utf8_unicode_ci'), nullable=False)
    description = db.Column(db.TEXT(collation='utf8_unicode_ci'), nullable=False)
    type = db.Column(db.VARCHAR(50, collation='utf8_unicode_ci'), nullable=False)
    format = db.Column(db.TEXT(collation='utf8_unicode_ci'), default=None)
    is_required = db.Column(TINYINT(1), nullable=False, default=0)
    is_delete = db.Column(TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column(db.DATETIME, default=datetime.now)
    mod_datetime = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)


class ItemQuestionAnswer(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    user_support_id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_question_id = db.Column(db.Integer, primary_key=True, nullable=False)
    value = db.Column(db.TEXT(collation='utf8_unicode_ci'), nullable=False)


class ItemShipping(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('item_shipping_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    project_item_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    user_support_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column('item_shipping_name', db.VARCHAR(500, collation='utf8_unicode_ci'), nullable=False)
    user_name_kana = db.Column('item_shipping_name_kana', db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    phone = db.Column('item_shipping_phone', db.VARCHAR(50, collation='utf8_unicode_ci'), nullable=False)
    zipcode = db.Column('item_shipping_zipcode', db.VARCHAR(50, collation='utf8_unicode_ci'), nullable=False)
    pref = db.Column('item_shipping_pref', db.VARCHAR(255, collation='utf8_unicode_ci'), nullable=False)
    town = db.Column('item_shipping_town', db.VARCHAR(500, collation='utf8_unicode_ci'), nullable=False)
    address = db.Column('item_shipping_address', db.VARCHAR(500, collation='utf8_unicode_ci'), nullable=False)
    building = db.Column('item_shipping_building', db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    tax = db.Column('item_shipping_tax', TINYINT(4), nullable=False, default=0)
    date = db.Column('item_shipping_date', db.DATE, nullable=False)
    status = db.Column('item_shipping_status', TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column('item_shipping_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('item_shipping_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)

    def __init__(self, project_item_id=None, project_id=None, user_support_id=None, user_id=None,
                 user_name=None, user_name_kana=None, phone=None, zipcode=None, pref=None,
                 town=None, address=None, building=None, tax=None, date=None, status=None,
                 reg_datetime=None, mod_datetime=None):
        address_key = current_app.config.get('ADDRESS_KEY')

        if project_item_id: self.project_item_id = project_item_id
        if project_id: self.project_id = project_id
        if user_support_id: self.user_support_id = user_support_id
        if user_id: self.user_id = user_id
        if user_name: self.user_name = func.to_base64(func.aes_encrypt(user_name, address_key))
        if user_name_kana: self.user_name_kana = func.to_base64(func.aes_encrypt(user_name_kana, address_key))
        if phone: self.phone = func.to_base64(func.aes_encrypt(phone, address_key))
        if zipcode: self.zipcode = func.to_base64(func.aes_encrypt(zipcode, address_key))
        if pref: self.pref = func.to_base64(func.aes_encrypt(pref, address_key))
        if town: self.town = func.to_base64(func.aes_encrypt(town, address_key))
        if address: self.address = func.to_base64(func.aes_encrypt(address, address_key))
        if building: self.building = func.to_base64(func.aes_encrypt(building, address_key))
        if tax: self.tax = tax
        if date: self.date = date
        if status: self.status = status
        if reg_datetime: self.reg_datetime = reg_datetime
        if mod_datetime: self.mod_datetime = mod_datetime

    def find(**kwargs):
        address_key = current_app.config.get('ADDRESS_KEY')
        engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')
        matadata = MetaData(bind=engine)
        item_shipping_c = Table('item_shipping', matadata, autoload=True)
        item_shipping_name_ = func.aes_decrypt(func.from_base64(item_shipping_c.c.item_shipping_name),
                                               address_key).label('user_name')
        item_shipping_name_kana_ = func.aes_decrypt(func.from_base64(item_shipping_c.c.item_shipping_name_kana),
                                                    address_key).label('user_name_kana')
        phone_ = func.aes_decrypt(func.from_base64(item_shipping_c.c.item_shipping_phone), address_key).label('phone')
        zipcode_ = func.aes_decrypt(func.from_base64(item_shipping_c.c.item_shipping_zipcode), address_key).label(
            'zipcode')
        pref_ = func.aes_decrypt(func.from_base64(item_shipping_c.c.item_shipping_pref), address_key).label('pref')
        town_ = func.aes_decrypt(func.from_base64(item_shipping_c.c.item_shipping_town), address_key).label('town')
        address_ = func.aes_decrypt(func.from_base64(item_shipping_c.c.item_shipping_address), address_key).label(
            'address')
        building_ = func.aes_decrypt(func.from_base64(item_shipping_c.c.item_shipping_building), address_key).label(
            'building')
        columns = [item_shipping_c.c.item_shipping_id,
                   item_shipping_c.c.project_item_id,
                   item_shipping_c.c.project_id,
                   item_shipping_c.c.user_support_id,
                   item_shipping_c.c.user_id,
                   item_shipping_name_,
                   item_shipping_name_kana_,
                   phone_,
                   zipcode_,
                   pref_,
                   town_,
                   address_,
                   building_,
                   item_shipping_c.c.item_shipping_tax,
                   item_shipping_c.c.item_shipping_date,
                   item_shipping_c.c.item_shipping_status]

        where_ = None
        if ('user_id' in kwargs) and ('user_support_id' in kwargs):
            where_ = and_(item_shipping_c.c.user_id == kwargs['user_id'],
                item_shipping_c.c.user_support_id == kwargs['user_support_id'])
        elif ('user_id' in kwargs):
            where_ = item_shipping_c.c.user_id == kwargs['user_id']

        elif ('user_support_id' in kwargs):
            where_ = item_shipping_c.c.user_support_id == kwargs['user_support_id']

        query = select().select_from(item_shipping_c).where(where_)
        user_shipping_ = query.with_only_columns(columns)
        results = db.session.execute(user_shipping_)
        shippings = []
        if results.rowcount > 0:
            for result in results:
                shipping = {}
                shipping['user_name'] = str(result.user_name, 'utf-8') if result.user_name else ''
                shipping['user_name_kana'] = str(result.user_name_kana,
                                                          'utf-8') if result.user_name_kana else''
                shipping['phone'] = str(result.phone, 'utf-8') if result.phone else ''
                shipping['zipcode'] = str(result.zipcode, 'utf-8') if result.zipcode else ''
                shipping['pref'] = str(result.pref, 'utf-8') if result.pref else ''
                shipping['town'] = str(result.town, 'utf-8') if result.town else ''
                shipping['address'] = str(result.address, 'utf-8') if result.address else ''
                shipping['building'] = str(result.building, 'utf-8') if result.building else ''
                shipping['id'] = result.item_shipping_id
                shipping['project_item_id'] = result.project_item_id
                shipping['project_id'] = result.project_id
                shipping['user_support_id'] = result.user_support_id
                shipping['user_id'] = result.user_id
                shipping['tax'] = result.item_shipping_tax
                shipping['date'] = result.item_shipping_date.strftime('%Y-%m-%d') if result.item_shipping_date else ''
                shipping['status'] = result.item_shipping_status
                shippings.append(shipping)
        return shippings


class User(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('user_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    gmo_member_id = db.Column('user_gmo_member_id', db.VARCHAR(60, collation='utf8_unicode_ci'), default=None)
    nick_name = db.Column('user_nick_name', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    name = db.Column('user_name', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    name_kana = db.Column('user_name_kana', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    image = db.Column('user_image', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    mail = db.Column('user_mail', db.VARCHAR(255, collation='utf8_unicode_ci'), unique=True, default=None)
    password = db.Column('user_password', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    birthday = db.Column('user_birthday', db.DATE, default=None)
    url1 = db.Column('user_url1', db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    url2 = db.Column('user_url2', db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    url3 = db.Column('user_url3', db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    url4 = db.Column('user_url4', db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    url5 = db.Column('user_url5', db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    introduction = db.Column('user_introduction', db.TEXT(collation='utf8_unicode_ci'))
    movie_code = db.Column('user_movie_code', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    received_magazin = db.Column('user_received_magazin', TINYINT(1), default=1)
    code = db.Column('user_code', db.VARCHAR(255, collation='utf8_unicode_ci'), default=None)
    memo = db.Column('user_memo', db.TEXT(collation='utf8_unicode_ci'))
    is_active = db.Column('user_is_active', TINYINT(1), nullable=False, default=0)
    is_retire = db.Column('user_is_retire', TINYINT(1), nullable=False, default=0)
    is_delete = db.Column('user_is_delete', TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column('user_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('user_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class UserAddress(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    zipcode = db.Column(db.VARCHAR(50, collation='utf8_unicode_ci'), default=None)
    phone = db.Column(db.VARCHAR(50, collation='utf8_unicode_ci'), default=None)
    pref = db.Column(db.VARCHAR(50, collation='utf8_unicode_ci'), default=None)
    town = db.Column(db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    address = db.Column(db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    building = db.Column(db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    full_name = db.Column(db.VARCHAR(500, collation='utf8_unicode_ci'), default=None)
    is_delete = db.Column(TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column(db.DATETIME, default=datetime.now)
    mod_datetime = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)

    def __init__(self, user_id=None, zipcode=None, phone=None, pref=None,
                 town=None, address=None, building=None, full_name=None, is_delete=None,
                 reg_datetime=None, mod_datetime=None):
        address_key = current_app.config.get('ADDRESS_KEY')

        self.user_id = user_id
        self.zipcode = func.to_base64(func.aes_encrypt(zipcode, address_key)) if zipcode else ''
        self.phone = func.to_base64(func.aes_encrypt(phone, address_key)) if phone else ''
        self.pref = func.to_base64(func.aes_encrypt(pref, address_key)) if pref else ''
        self.town = func.to_base64(func.aes_encrypt(town, address_key)) if town else ''
        self.address = func.to_base64(func.aes_encrypt(address, address_key)) if address else ''
        self.building = func.to_base64(func.aes_encrypt(building, address_key)) if building else ''
        self.full_name = func.to_base64(func.aes_encrypt(full_name, address_key)) if full_name else ''
        self.is_delete = is_delete
        self.reg_datetime = reg_datetime if reg_datetime else None
        self.mod_datetime = mod_datetime if mod_datetime else None

    def find(**kwargs):
        address_key = current_app.config.get('ADDRESS_KEY')
        engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')
        metadata = MetaData(bind=engine)
        user_address_c = Table('user_address', metadata, autoload=True)

        zipcode_ = func.aes_decrypt(func.from_base64(user_address_c.c.zipcode), address_key).label('zipcode')
        phone_ = func.aes_decrypt(func.from_base64(user_address_c.c.phone), address_key).label('phone')
        pref_ = func.aes_decrypt(func.from_base64(user_address_c.c.pref), address_key).label('pref')
        town_ = func.aes_decrypt(func.from_base64(user_address_c.c.town), address_key).label('town')
        address_ = func.aes_decrypt(func.from_base64(user_address_c.c.address), address_key).label('address')
        building_ = func.aes_decrypt(func.from_base64(user_address_c.c.building), address_key).label('building')
        full_name_ = func.aes_decrypt(func.from_base64(user_address_c.c.full_name), address_key).label('full_name')

        columns = [user_address_c.c.id,
                   user_address_c.c.user_id,
                   zipcode_,
                   phone_,
                   pref_,
                   town_,
                   address_,
                   building_,
                   full_name_,
                   user_address_c.c.is_delete]

        query = select().select_from(user_address_c)
        if ('user_id' in kwargs):
            query = query.where(user_address_c.c.user_id == kwargs['user_id'])

        user_address_ = query.with_only_columns(columns)
        results = db.session.execute(user_address_)
        addresses = []
        if results.rowcount > 0:
            for result in results:
                address = {}
                address['zipcode'] = str(result.zipcode, 'utf-8') if result.zipcode else ''
                address['phone'] = str(result.phone, 'utf-8') if result.phone else ''
                address['pref'] = str(result.pref, 'utf-8') if result.pref else ''
                address['town'] = str(result.town, 'utf-8') if result.town else ''
                address['address'] = str(result.address, 'utf-8') if result.address else ''
                address['building'] = str(result.building, 'utf-8') if result.building else ''
                address['full_name'] = str(result.full_name, 'utf-8') if result.full_name else ''
                address['id'] = result.id
                address['user_id'] = result.user_id
                address['is_delete'] = result.is_delete
                addresses.append(address)
        return addresses


class UserCard(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('user_card_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    code = db.Column('user_card_code', db.CHAR(4, collation='utf8_unicode_ci'), nullable=False)
    seq = db.Column('user_card_seq', TINYINT(1), nullable=False)
    forward = db.Column('user_card_forward', db.VARCHAR(20, collation='utf8_unicode_ci'), nullable=False)
    is_delete = db.Column('user_card_is_delete', TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column('user_card_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('user_card_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class UserSupport(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column('user_support_id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    project_item_id = db.Column(db.Integer, nullable=False, default=0)
    order_id = db.Column('user_support_order_id', db.VARCHAR(30, collation='utf8_unicode_ci'), default=None)
    amount = db.Column('user_support_amount', db.Integer, nullable=False)
    status = db.Column('user_support_status', TINYINT(1), default=1)
    payment_type = db.Column('user_support_payment_type', db.VARCHAR(50))
    device = db.Column('user_support_device', db.VARCHAR(50))
    is_delete = db.Column('user_support_is_delete', TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column('user_support_reg_datetime', db.DATETIME, default=datetime.now)
    mod_datetime = db.Column('user_support_mod_datetime', db.DATETIME, default=datetime.now, onupdate=datetime.now)


class FavoriteCreator(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    creator_id = db.Column(db.Integer, primary_key=True, nullable=False)
    checked = db.Column(TINYINT(1), nullable=False, default=0)
    mod_datetime = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)


class MailMagazine(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    category = db.Column(db.VARCHAR(50), primary_key=True, nullable=False)
    checked = db.Column(TINYINT(1), nullable=False, default=0)
    mod_datetime = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)


class Member(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    id = db.Column(db.VARCHAR(20), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, default=None)
    status = db.Column(db.Enum('REG', 'OWN', 'OPE'), nullable=False, default='REG')
    nickname = db.Column(db.VARCHAR(360), nullable=False)
    birthday = db.Column(db.DATE, default=None)
    gender = db.Column(db.Enum('M', 'F'), nullable=False, default='M')
    pref_code = db.Column(db.VARCHAR(2), nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)
    email_status = db.Column(db.Enum('DELIVERY', 'UNDELIVERY', 'STOP'), nullable=False, default='STOP')
    email_permission = db.Column(db.Enum('VLD', 'STP'), nullable=False, default='STP')
    session_key = db.Column(db.VARCHAR(255), default=None)
    is_delete = db.Column(TINYINT(1), nullable=False, default=0)
    reg_datetime = db.Column(db.DATETIME, default=datetime.now)
    mod_datetime = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)


class MemberTracking(db.Model):
    __table_args__ = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})
    tracking_id = db.Column(db.VARCHAR(200), primary_key=True, nullable=False)
    member_id = db.Column(db.VARCHAR(20), primary_key=True, nullable=False)
    is_delete = db.Column(TINYINT(1), nullable=False, default=0)
    mod_datetime = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)

# class Entry(db.Model):
#     __tablename__ = 'entries'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.Text)
#     text = db.Column(db.Text)
#
#     def __repr__(self):
#         return '<Entry id={id} title={title!r}>'.format(
#                 id=self.id, title=self.title)

def init():
    db.create_all()
