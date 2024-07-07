from flask import Flask, request, jsonify, render_template, url_for, redirect, flash, make_response
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
import managers.database as database
from sqlite3 import IntegrityError
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['JWT_SECRET_KEY'] = '3a18fe56-9592-428d-8704-79ad1eae357b'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Set to True for additional security
jwt = JWTManager(app)


def jwt_required_redirect(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    user = database.get_user_by_username(username)
    if user and check_password_hash(user[1], password):
        access_token = create_access_token(identity=username)
        response = make_response(redirect(url_for('dashboard')))
        set_access_cookies(response, access_token, max_age=15 * 60)
        flash('Login successful!', 'success')
        return response
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if len(username) == 0 or len(password) == 0:
        return "You need to provide both username and password", 401

    hashed_password = generate_password_hash(password)
    try:
        database.add_user(username, hashed_password)
    except IntegrityError:
        return jsonify({"msg": "User already exists"}), 400

    return jsonify({"msg": "User created successfully"}), 201


@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    flash('Logged out successfully!', 'success')
    return response


@app.route('/dashboard', methods=['GET'])
@jwt_required_redirect
def dashboard():
    current_user = get_jwt_identity()
    return render_template('dashboard.html', username=current_user, database=database)


@app.route('/create_new_issue', methods=['POST', 'GET'])
def create_new_issue():
    print('pusty print')
    if request.method == 'GET':
        return render_template('create_new_issue.html')

    title = request.form.get('title')
    description = request.form.get('description')
    print(title, description)
    database.add_task(description, "test_org_0")
    return redirect(url_for('create_new_issue'))


@app.route('/get_tasks')
def get_tasks():
    org = request.args.get('org')
    tasks = database.get_tasks_for_organization(org)  # Replace with actual database logic
    print(tasks)
    tasks_data = [
        {
            'task_id': task.task_id,
            'assigned_to': task.assigned_to,
            'description': task.description,
            'title': task.title
        } for task in tasks
    ]
    return jsonify({'tasks': tasks_data})


if __name__ == '__main__':
    app.run(debug=True)
