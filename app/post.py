from .imports import *

post = Blueprint('post', __name__)


@post.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = database.get_user_by_username(username)
    if user and check_password_hash(user[1], password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        response = make_response(redirect(url_for('get.dashboard')))
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('get.login'))


@post.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    response = jsonify({"msg": "Token refreshed"})
    set_access_cookies(response, access_token)
    return response


@post.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if len(username) == 0 or len(password) == 0:
        flash("User already exists")
        return redirect(url_for('You need to provide both username and password'))

    hashed_password = generate_password_hash(password)
    try:
        database.add_user(username, hashed_password)
    except IntegrityError:
        flash("User already exists")
        return redirect(url_for('get.register'))

    return redirect(url_for('get.login'))


@post.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = make_response(redirect(url_for('get.login')))
    unset_jwt_cookies(response)
    flash('Logged out successfully!', 'success')
    return response


@post.route('/create_new_issue', methods=['POST'])
@jwt_required_redirect
def create_new_issue():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        organization = request.form.get('organization_name')
        status = int(request.form.get('status'))
        priority = int(request.form.get('priority'))
        database.add_task(status, description, organization, priority, title)
        return redirect(url_for('get.dashboard'))
    except Exception as error:
        flash(str(error), 'warning')
        return redirect(url_for('get.create_new_issue'))


@post.route('/get_tasks', methods=['POST'])
@jwt_required_redirect_json
def get_tasks():
    tasks = database.get_tasks_for_organization(request.json.get('org'))
    tasks_data = [
        {
            'task_id': task.task_id,
            'assigned_to': task.assigned_to,
            'description': task.description,
            'title': task.title,
            'priority': task.priority
        } for task in tasks
    ]
    tasks_data = sorted(tasks_data, key=lambda x: x['priority'])
    return jsonify({'status': True, 'tasks': tasks_data})


@post.route('/get_task', methods=['POST'])
@jwt_required_redirect_json
def get_task():
    task = database.get_task_by_id(request.json.get('task_id'))
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    tasks_data = {
        'task_id': task.task_id,
        'assigned_to': id_list[task.assigned_to],
        'description': task.description,
        'title': task.title,
        'priority': task.priority
    }
    return jsonify({'status': True, 'task': tasks_data})


@post.route('/get_orgs', methods=['POST'])
@jwt_required_redirect_json
def get_orgs():
    orgs = database.get_user_orgs(username=get_jwt_identity())
    return jsonify({'status': True, 'orgs': orgs})


@post.route('/update_task_status', methods=['POST'])
@jwt_required_redirect_json
def update_task_status():
    try:
        database.update_task_table(request.json['task_id'], table_list[request.json['new_status']])
        return jsonify({'status': True})
    except Exception as error:
        return jsonify({'status': False, 'error': str(error)})


@post.route('/join_org', methods=['POST'])
@jwt_required_redirect_json
def join_org():
    username   = get_jwt_identity()
    org_name   = request.json['orgName']
    org_passwd = request.json['orgPassword']

    user_orgs = database.get_user_orgs(username)

    if org_passwd in user_orgs:
        return jsonify({'status': False, 'error': 'User is already assigned to that org'})

    org = database.get_org_by_org_name(org_name)
    if org and check_password_hash(org[1], org_passwd):
        try:
            database.assign_user_to_organization(username, org_name)
            return jsonify({'status': True})
        except IntegrityError:
            return jsonify({'status': False, 'error': 'User is already part of this organization'})
    else:
        flash('Invalid org name or password' 'danger')
        return jsonify({'status': False, 'error': 'Invalid org name or password'})


@post.route('/create_org', methods=['POST'])
@jwt_required_redirect_json
def create_org():
    username   = get_jwt_identity()
    org_name   = request.json['orgName']
    org_passwd = request.json['orgPassword']

    hashed_password = generate_password_hash(org_passwd)
    try:
        database.add_organization(org_name, hashed_password)
    except IntegrityError:
        return jsonify({'status': False, "msg": "Organization already exists"}), 400

    database.assign_user_to_organization(username, org_name, 5)
    return jsonify({'status': True, "msg": "Organization created successfully"}), 201


@post.route('/delete_task', methods=['POST'])
@jwt_required_redirect_json
def delete_task():
    username = get_jwt_identity()
    user_orgs = database.get_user_orgs(username)
    task_id = request.json.get('task_id')
    org_task = database.get_org_by_org_task_id(task_id)

    if org_task not in user_orgs:
        return jsonify({'status': False, "msg": "User is not in org related to task"}), 400

    if database.get_user_access_level(username, org_task) < 5:
        return jsonify({'status': False, "msg": "You don't have enough permission to delete tasks!"}), 400

    database.delete_task(task_id)
    return jsonify({'status': True}), 201


@post.route('/view_all_tasks', methods=['POST'])
@jwt_required_redirect
def view_all_tasks():
    current_user = get_jwt_identity()
    task_to_assign = request.form.get('assign_button')
    if current_user not in database.get_users_from_task(task_to_assign):
        database.add_user_to_task(current_user, task_to_assign)
    response = make_response(redirect(url_for('get.view_all_tasks')))
    return response