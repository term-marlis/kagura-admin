from flask import request, redirect, url_for, render_template, flash, abort, \
        jsonify

# from flask import Blueprint, render_template, request, url_for, flash, current_app, g, jsonify, session, Response, abort

from flaskr import app, db
from flaskr.models import User, Project, Information, Admin
from flaskr import converter
from flaskr.form import ProjectBasicForm
from flaskr import decorator



# @app.route('/add', methods=['POST'])
# def add_entry():
#     entry = Entry(
#             title=request.form['title'],
#             text=request.form['text']
#             )
#     db.session.add(entry)
#     db.session.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))

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


# @app.route('/admin/information/<int:information_id>/delete', methods=['DELETE'])
# @decorator.managed_session()
# def information_delete(information_id):
#     information = Information.query.get(information_id)
#     if information is None:
#         return render_template('information_list.html', information=None)
#         # response = jsonify({'status': 'Not Found'})
#         # response.status_code = 404
#         # return response
#     db.session.delete(information)
#     # return jsonify({'status': 'OK'})
#     return render_template('information_list.html', information=information)
#
#
# @app.route('/admin/information/<int:information_id>/edit', methods=['POST'])
# @decorator.managed_session()
# def information_edit():
#     pass
#
#
# @app.route('/admin/information/list')
# def information_list():
#     pass
#
#
# @app.route('/admin/information/preview')
# def information_preview():
#     pass


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
    project = Project.query.get(project_id)
    if project is None:
        return render_template('admin/project_list.html', project=None)
    project.is_approval = 1
    project.public_status = 2
    db.session.add(project)
    return render_template('admin/project_list.html', project=project)


@app.route('/project/<int:project_id>/delete', methods=['DELETE'])
@decorator.managed_session()
def project_delete(project_id):
    project = Project.query.get(project_id)
    if project is None:
        return render_template('project_list.html', project=None)
    db.session.delete(project)
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
        return redirect(url_for('/admin/users/%s' % user_id))
    return render_template('admin/user_edit.html', user=user)


@app.route('/project/<int:project_id>/edit', methods=['POST'])
@decorator.managed_session()
def project_edit():
    pass


@app.route('/project/end/list')
def project_end_list():
    pass


@app.route('/project/no_approve/list')
def project_no_approve_list():
    pass


@app.route('/project/list')
def project_list():
    basic_form = ProjectBasicForm(request.form)
    project_ = converter.project_form_to_api_project(basic_form)
    projects = Project.query.filter_by(is_approval=project_.is_approval).order_by(Project.reg_datetime.desc()).limit(10).all()
    return render_template('admin/project_list.html', project=project_)


@app.route('/project/memo/detail')
def project_memo_detal():
    pass


@app.route('/project/republic', methods=['PUT'])
@decorator.managed_session()
def project_republic():
    pass


@app.route('/project/running/list')
def project_running_list():
    pass


@app.route('/project/sucess/list')
def project_success_list():
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


@app.route('/project/unsuccess/list')
def project_unsuccess_list():
    pass


@app.route('/project/waiting/list')
def project_waiting_list():
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
