from .imports import *

get = Blueprint('get', __name__)


@get.route('/')
def home():
    return redirect(url_for('get.login'))


@get.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@get.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@get.route('/dashboard', methods=['GET'])
@jwt_required_redirect
def dashboard():
    current_user = get_jwt_identity()
    return render_template('dashboard.html', username=current_user)


@get.route('/create_new_issue', methods=['GET'])
@jwt_required_redirect
def create_new_issue():
    current_user = get_jwt_identity()
    return render_template('create_new_issue.html', username=current_user, database=database)


@get.route('/view_all_tasks', methods=['GET'])
@jwt_required_redirect
def view_all_tasks():
    current_user = get_jwt_identity()
    return render_template("view_all_tasks.html", username=current_user, database=database)





