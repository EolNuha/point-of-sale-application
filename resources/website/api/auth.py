from flask import Blueprint, request, jsonify, make_response, current_app
from website.models.user import User
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from website import db
from website.helpers import getPaginatedDict
from website.jsonify.user import getUsersList, getUserDict
from website.token import token_required
from sqlalchemy import or_, asc, desc, and_

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/signin', methods=['POST'])
def signin():
    email = request.json["email"]
    password = request.json["password"]
  
    if not email or not password:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Signin required!"'}
        )
  
    user = User.query\
        .filter(or_(
        User.username.ilike(email),
        User.email.ilike(email),
        )).first()
  
    if not user:
        return make_response(
            'userWithThisEmailDoesNotExist',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist!"'}
        )
  
    if check_password_hash(user.password, password):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(days = 1)
        }, current_app.config['SECRET_KEY'])
  
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    
    return make_response(
            'passwordIncorrect',
            403,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist!"'}
        )
  
@auth_api.route('/signup', methods=['POST'])
def signup():
    email = request.json["email"]
    password = request.json["password"]
    first_name = request.json["firstName"]
    last_name = request.json["lastName"]
    username = request.json["username"]
    user_role = request.json["userRole"]

    user = User.query\
        .filter_by(email = email)\
        .first()

    if not user:
        user = User(
            public_id = str(uuid.uuid4()),
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            user_role = user_role or "staff",
            password = generate_password_hash(password),
            date_created=datetime.now(),
            date_modified=datetime.now(),
        )

        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        return make_response('userExists', 500)



@auth_api.route('/users', methods=['GET'])
def users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '*', type=str)
    sort_column = request.args.get('sort_column', "id", type=str)
    sort_dir = request.args.get('sort_dir', "desc", type=str)
    active = [x == 'true' for x in request.args.getlist('active[]')]
    if not active: active = [True, False]

    sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

    if '*' in search or '_' in search: 
        looking_for = search.replace('_', '__')\
            .replace('*', '%')\
            .replace('?', '_')
    else:
        looking_for = '%{0}%'.format(search)
        
    paginated_items = User.query.filter(or_(
        User.first_name.ilike(looking_for),
        User.last_name.ilike(looking_for),
        User.id.ilike(looking_for),
        User.username.ilike(looking_for),
        User.email.ilike(looking_for),
        ))\
        .filter(and_(User.active.in_(active)))\
        .order_by(sort)\
        .paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getUsersList(paginated_items.items), paginated_items))

@auth_api.route('/users/<int:id>', methods=['GET'])
@token_required
def getUserDetails(id):
    return jsonify(getUserDict(User.query.filter_by(id=id).first()))

@auth_api.route('/users/<int:id>', methods=['PUT'])
@token_required
def updateUserDetails(id):
    email = request.json["email"]
    first_name = request.json["firstName"]
    last_name = request.json["lastName"]
    username = request.json["username"]
    user_role = request.json["userRole"]
    active = request.json["active"]
    user = User.query.filter_by(id=id).first()

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.username = username
    user.user_role = user_role
    user.active = active
    user.date_modified = datetime.now()

    db.session.commit()

    return "Success", 200

@auth_api.route('/users/<int:id>', methods=["DELETE"])
def deleteUser(id):
    user = User.query.filter_by(id=id).first()
    if user.sales or user.purchases:
        return "This user can not be deleted because it has sales or purchases connected to it!", 500
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return "Success", 200

@auth_api.route('/verify-token', methods=['POST'])
@token_required
def verify_token():
    return jsonify({'success': True}), 200

@auth_api.route('/current-user')
@token_required
def currentUser():
    token = request.headers['x-access-token']
    data = jwt.decode(token, current_app.config['SECRET_KEY'])
    return jsonify(getUserDict(User.query\
        .filter_by(public_id = data['public_id'])\
        .first_or_404()))

@auth_api.before_app_first_request
def createDemoUsers():
    if (User.query.count() > 0):
        return
    demo = [
        ["eol", "nuha", "eolnuha", "eol@gmail.com", "superadmin"],
    ]
    for i in demo:
        db.session.add(User(
            public_id=str(uuid.uuid4()),
            first_name=i[0], 
            last_name=i[1], 
            username=i[2], 
            email=i[3], 
            password=generate_password_hash("admin"), 
            user_role=i[4],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            ))
        db.session.commit()
    return "success", 200