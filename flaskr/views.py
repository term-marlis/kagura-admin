from flask import request, redirect, url_for, render_template, flash, abort, \
        jsonify
from flaskr import app, db
from flaskr.models import User, Project, Information, Admin
from flaskr import converter
from flaskr.form import ProjectBasicForm
from flaskr import decorator

from flask import current_app
from sqlalchemy.sql import select

from flaskr.sql_parts.abstract_parts import AbstractParts
from flaskr.sql_parts.project_list import ProjectList
from flaskr.sql_parts.project_end_list import ProjectEndList
from flaskr.sql_parts.project_no_approve_list import ProjectNoApproveList
from flaskr.sql_parts.project_running_list import ProjectRunningList
from flaskr.sql_parts.project_success_list import ProjectSuccessList
from flaskr.sql_parts.project_un_success_list import ProjectUnSuccessList
from flaskr.sql_parts.project_waiting_list import ProjectWaitingList


@app.route('/')
@decorator.managed_session()
def top():
    """ トップ画面 """
    projects = Project.query.filter_by(is_approval=0).order_by(Project.reg_datetime.desc()).limit(10).all()
    return render_template('admin/index.html', projects=projects)


@app.route('/admin/<int:admin_id>/delete', methods=['DELETE'])
@decorator.managed_session()
def admin_delete(admin_id):
    """ Admin削除 """
    admin = Admin.query.get(admin_id)
    if admin is None:
        return render_template('admin/admin_list.html', admin=None)
    db.session.delete(admin)
    return render_template('admin/admin_list.html', admin=admin)

@app.route('/admin/<int:admin_id>/edit', methods=['POST'])
@decorator.managed_session()
def admin_edit(admin_id):
    """ passwordリセット """
    pass


@app.route('/admin/list', methods=['GET', 'POST'])
def admin_list():
    print('sss')
    admin = Admin.query
    print(request.form)

    input_login_email = None
    input_role = None
    if request.form:
        if request.form['login_email']:
            # keyword
            input_login_email = request.form['login_email']
            admin = admin.filter(Admin.login_email.like('%' + str(request.form['login_email']) + '%'))
        if request.form['role']:
            # role
            input_role = request.form['role']
            admin = admin.filter(Admin.role == request.form['role'])
    admins = admin.all()
    return render_template('admin/admin_list.html', admins=admins, input_login_email=input_login_email, input_role=input_role)


@app.route('/admin/download')
def download():
    pass


@app.route('/login/user')
def login_user():
    pass


@app.route('/login')
def login():
    pass


@app.route('/logout')
def logout():
    pass


@app.route('/project/approve')
@decorator.managed_session()
def project_approve(project_id):
    """ プロジェクト承認 """
    project = Project.query.get(project_id)
    if project is None:
        return render_template('admin/project_list.html', project=None)
    project.is_approval = 1
    project.public_status = 2
    db.session.add(project)
    db.session.commit()

    # TODO 承認後　メール送信

    return render_template('admin/project_list.html', project=project)


@app.route('/project/<int:project_id>/delete', methods=['DELETE'])
@decorator.managed_session()
def project_delete(project_id):
    """ プロジェクト削除 """


    print('+'*100)
    project_ = Project.query.filter_by(id=project_id, is_delete=0).scalar()
    if project_ is None:
        return render_template('project_list.html', project=None)

    reports_ = ProjectReport.query.filter_by(project_id=project_id).all()
    for report in reports_: db.session.delete(report)

    faqs_ = ProjectFaq.query.filter_by(project_id=project_id).all()
    for faq in faqs_: db.session.delete(faq)

    items_ = ProjectItem.query.filter_by(project_id=project_id, is_delete=0).all()
    if items_:
        for item in items_:
            questions_ = ItemQuestion.query.filter_by(project_item_id=item.id, is_delete=0).all()
            for question in questions_:
                question.is_delete = 1
                db.session.add(question)
            item.is_delete = 1
            db.session.add(item)
    project_.is_delete = 1
    db.session.add(project_)
    db.session.commit()
    return render_template('admin/project_list.html', project=project)


@app.route('/project/<int:project_id>/status/edit', methods=['POST'])
@decorator.managed_session()
def project_status_edit(project_id):

    # 入力チェック
    # basic_form = ProjectBasicForm(request.form)
    # data = converter.project_form_to_api_project(basic_form)

    project = Project.query.get(project_id)
    if project is None:
        abort(404)
    if request.method == 'POST':
        if projct.is_approval and projct.is_approval != request.form['is_approval']:
            # 承認メール送信
            if projct.is_approval == 1:
                pass
            if projct.is_approval == 2:
                pass
        if projct.is_approval and projct.public_status != request.form['public_status']:
            #
            if projct.public_status == 2:
                pass
            if projct.public_status != 2:
                project.popular_order = 0
        if projct.is_delete and projct.is_delete == 1:
            project.popular_order = 0

        project.name=request.form['name']
        project.email=request.form['email']
        if request.form['password']:
            user.password=request.form['password']
        db.session.add(project)
        db.session.commit()

        return redirect(url_for('/admin/users/%s' % user_id))
    return render_template('admin/user_edit.html', user=user)


@app.route('/project/<int:project_id>/edit', methods=['POST'])
@decorator.managed_session()
def project_edit():
    """ プロジェクトイメージを更新している """
    pass


@app.route('/project/list', methods=['GET', 'POST'])
def project_list():
    # basic_form = ProjectBasicForm(request.form)
    # project_ = converter.project_form_to_api_project(basic_form)
    engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    parts = eval('ProjectList')
    project_list_ = parts(engine)
    project_list_.select()
    project_list_.from_table()
    project_list_.where(request.form)
    project_list_.group_by()
    print(project_list_.query)
    projects = db.session.execute(project_list_.query)
    if projects is None:
        return render_template('admin/project_list.html', projects=None)
    return render_template('admin/project_list.html', projects=projects)


@app.route('/project/no_approve/list')
def project_no_approve_list():
    engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    parts = eval('ProjectNoApproveList')
    project_list_ = parts(engine)
    project_list_.select()
    project_list_.from_table()
    project_list_.where(request.form)
    project_list_.group_by()
    print(project_list_.query)
    projects = db.session.execute(project_list_.query)
    if projects is None:
        return render_template('admin/project_list.html', projects=None)
    return render_template('admin/project_list.html', projects=projects)


@app.route('/project/waiting/list')
def project_waiting_list():
    engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    parts = eval('ProjectWaitingList')
    project_list_ = parts(engine)
    project_list_.select()
    project_list_.from_table()
    project_list_.where(request.form)
    project_list_.group_by()
    print(project_list_.query)
    projects = db.session.execute(project_list_.query)
    if projects is None:
        return render_template('admin/project_list.html', projects=None)
    return render_template('admin/project_list.html', projects=projects)


@app.route('/project/running/list')
def project_running_list():
    engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    parts = eval('ProjectRunningList')
    project_list_ = parts(engine)
    project_list_.select()
    project_list_.from_table()
    project_list_.where(request.form)
    project_list_.group_by()
    print(project_list_.query)
    projects = db.session.execute(project_list_.query)
    if projects is None:
        return render_template('admin/project_list.html', projects=None)
    return render_template('admin/project_list.html', projects=projects)


@app.route('/project/success/list')
def project_success_list():
    engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    parts = eval('ProjectSuccessList')
    project_list_ = parts(engine)
    project_list_.select()
    project_list_.from_table()
    project_list_.where(request.form)
    project_list_.group_by()
    print(project_list_.query)
    projects = db.session.execute(project_list_.query)
    if projects is None:
        return render_template('admin/project_list.html', projects=None)
    return render_template('admin/project_list.html', projects=projects)


@app.route('/project/un_success/list')
def project_un_success_list():
    engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    parts = eval('ProjectUnSuccessList')
    project_list_ = parts(engine)
    project_list_.select()
    project_list_.from_table()
    project_list_.where(request.form)
    project_list_.group_by()
    print(project_list_.query)
    projects = db.session.execute(project_list_.query)
    if projects is None:
        return render_template('admin/project_list.html', projects=None)
    return render_template('admin/project_list.html', projects=projects)

@app.route('/project/end/list')
def project_end_list():
    """ プロジェクト終了リスト """

    projects = _list()
    if projects is None:
        return render_template('admin/project_list.html', projects=None)
    return render_template('admin/project_list.html', projects=projects)


def _list():
    engine = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    parts = eval('ProjectEndList')
    project_list_ = parts(engine)
    project_list_.select()
    project_list_.from_table()
    project_list_.where(request.form)
    project_list_.group_by()
    print(project_list_.query)
    projects = db.session.execute(project_list_.query)


@app.route('/project/memo/detail')
def project_memo_detal():
    pass


@app.route('/project/republic', methods=['PUT'])
@decorator.managed_session()
def project_republic():
    pass




@app.route('/project/support/edit', methods=['POST'])
@decorator.managed_session()
def project_support_edit():
    pass


@app.route('/project/supportor')
def project_supportor():
    pass


@app.route('/project/unpublic', methods=['PUT'])
@decorator.managed_session()
def project_unpublic():
    pass


@app.route('/user/<int:user_id>/delete/', methods=['DELETE'])
@decorator.managed_session()
def user_delete(user_id):
    user = User.query.get(user_id)
    if user is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(user)
    return jsonify({'status': 'OK'})


@app.route('/user/<int:user_id>/status/edit', methods=['POST'])
@decorator.managed_session()
def user_status_edit():
    pass


@app.route('/user/<int:user_id>/edit/', methods=['POST'])
@decorator.managed_session()
def user_edit(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if request.method == 'POST':
        user.name=request.form['name']
        user.email=request.form['email']
        if request.form['password']:
            user.password=request.form['password']
        db.session.add(user)
        return redirect(url_for('user_detail', user_id=user_id))
    return render_template('user/edit.html', user=user)


@app.route('/user/list')
def user_list():

    admin = User.query
    if request.form['gmo_member_id']:
        # gmo_member_id
        admin = admin.filter(Admin.role == request.form['gmo_member_id'])
    if request.form['nick_name']:
        # nick_name
        admin = admin.filter(Admin.nick_name.like("%s")) % request.form['nick_name']
    if request.form['mail']:
        # mail
        admin = admin.filter(Admin.mail.like("%s")) % request.form['mail']

    if request.form['start_birthday'] and request.form['end_birthday']:
        # user birthday
        admin = admin.filter(User.birthday > request.form['start_birthday'])
        admin = admin.filter(User.birthday < request.form['end_birthday'])
    if request.form['gender']:
        # gender
        admin = admin.filter(Member.gender == request.form['gender'])

    if request.form['start_reg_datetime'] and request.form['end_reg_datetime']:
        # user reg_datetime
        admin = admin.filter(User.reg_datetime > request.form['start_reg_datetime'])
        admin = admin.filter(User.reg_datetime < request.form['end_reg_datetime'])

    if request.form['user_support_status']:
        # user_support
        admin = admin.filter(UserSupport.status == request.form['user_support_status'])

    if request.form['member_status']:
        # user_support
        admin = admin.filter(Member.status == request.form['member_status'])

    users = User.query.all()
    return render_template('user/list.html', users=users)


@app.route('/user/<int:user_id>/')
def user_detail(user_id):
    user = User.query.get(user_id)
    return render_template('user/detail.html', user=user)


@app.route('/user/create/', methods=['GET', 'POST'])
@decorator.managed_session()
def user_create():
    if request.method == 'POST':
        user = User(name=request.form['name'],
                    email=request.form['email'],
                    password=request.form['password'])
        db.session.add(user)
        return redirect(url_for('user_list'))
    return render_template('user/edit.html')


@app.route('/user/project/list')
def user_project_list():
    pass
