from flask import request, redirect, url_for, render_template, flash, abort, \
        jsonify

# from flask import Blueprint, render_template, request, url_for, flash, current_app, g, jsonify, session, Response, abort

from flaskr import app, db
from flaskr.models import User, Project, Information, Admin
from flaskr import converter
from flaskr.form import ProjectBasicForm



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


@app.route('/admin/')
def top():
    projects = Project.query.filter_by(is_approval=0).order_by(Project.reg_datetime.desc()).limit(10).all()
    return render_template('admin/index.html', projects=projects)


@app.route('/admin/<int:admin_id>/delete', methods=['DELETE'])
def admin_delete(admin_id):
    admin = Admin.query.get(admin_id)
    if admin is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.route('/admin/<int:admin_id>/edit')
def admin_edit(admin_id):
    pass


@app.route('/admin/list')
def admin_list():
    pass


@app.route('/admin/download')
def download():
    pass


@app.route('/admin/information/<int:information_id>/delete')
def information_delete(information_id):
    information = Information.query.get(information_id)
    if admin is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(information)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.route('/admin/information/<int:information_id>/edit')
def information_edit():
    pass


@app.route('/admin/information/list')
def information_list():
    pass


@app.route('/admin/information/preview')
def information_preview():
    pass


@app.route('/admin/login/user')
def login_user():
    pass


@app.route('/admin/login')
def login():
    pass


@app.route('/admin/logout')
def logout():
    pass


@app.route('/admin/project/approve')
def project_approve():
    pass


@app.route('/admin/project/<int:project_id>/delete', methods=['DELETE'])
def project_delete(project_id):
    project = Project.query.get(project_id)
    if project is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(project)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.route('/admin/project/<int:project_id>/status/edit', methods=['GET', 'POST'])
def project_status_edit(project_id):
    project = Project.query.get(project_id)
    if project is None:
        abort(404)
    if request.method == 'POST':
        project.name=request.form['name']
        project.email=request.form['email']
        if request.form['password']:
            user.password=request.form['password']
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user_id))
    return render_template('user/edit.html', user=user)


@app.route('/admin/project/<int:project_id>/edit')
def project_edit():
    pass


@app.route('/admin/project/end/list')
def project_end_list():
    pass


@app.route('/admin/project/no_approve/list')
def project_no_approve_list():
    pass


@app.route('/admin/project/list')
def project_list():
    basic_form = ProjectBasicForm(request.form)
    project_ = converter.project_form_to_api_project(basic_form)
    projects = Project.query.filter_by(is_approval=project_.is_approval).order_by(Project.reg_datetime.desc()).limit(10).all()
    return render_template('admin/project_list.html', project=project_)


@app.route('/admin/project/memo/detail')
def project_memo_detal():
    pass


@app.route('/admin/project/republic')
def project_republic():
    pass


@app.route('/admin/project/running/list')
def project_running_list():
    pass


@app.route('/admin/project/sucess/list')
def project_success_list():
    pass


@app.route('/admin/project/support/edit')
def project_support_edit():
    pass


@app.route('/admin/project/supportor')
def project_supportor():
    pass


@app.route('/admin/project/unpublic')
def project_unpublic():
    pass


@app.route('/admin/project/unsuccess/list')
def project_unsuccess_list():
    pass


@app.route('/admin/project/waiting/list')
def project_waiting_list():
    pass


@app.route('/admin/users/<int:user_id>/delete/', methods=['DELETE'])
def user_delete(user_id):
    user = User.query.get(user_id)
    if user is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.route('/admin/users/<int:user_id>/status/edit')
def user_status_edit():
    pass


@app.route('/admin/users/<int:user_id>/edit/', methods=['GET', 'POST'])
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
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user_id))
    return render_template('user/edit.html', user=user)


@app.route('/admin/users/list')
def user_list():
    users = User.query.all()
    return render_template('user/list.html', users=users)


@app.route('/admin/users/<int:user_id>/')
def user_detail(user_id):
    user = User.query.get(user_id)
    return render_template('user/detail.html', user=user)


@app.route('/admin/users/create/', methods=['GET', 'POST'])
def user_create():
    if request.method == 'POST':
        user = User(name=request.form['name'],
                    email=request.form['email'],
                    password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_list'))
    return render_template('user/edit.html')


@app.route('/admin/user/projects/list')
def user_project_list():
    pass

