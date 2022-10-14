from flask import Flask, Blueprint, request, jsonify, make_response, current_app
from website.models import User
import uuid
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from website import db
from website.helpers import getUsersList, getUserDict, getPaginatedDict
from website.token import token_required, currentUser
from sqlalchemy import or_

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['POST'])
def signin():
    email = request.json["email"]
    password = request.json["password"]
  
    if not email or not password:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Signin required !!"'}
        )
  
    user = User.query\
        .filter_by(email = email)\
        .first()
  
    if not user:
        return make_response(
            'User with this email does not exist!',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if check_password_hash(user.password, password):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(days = 365)
        }, current_app.config['SECRET_KEY'])
  
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
            'Password is incorrect!',
            403,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
# signup route
@auth.route('/signup', methods=['POST'])
def signup():
    email = request.json["email"]
    password = request.json["password"]
    first_name = request.json["firstName"]
    last_name = request.json["lastName"]
    username = request.json["username"]
    user_type = request.json["userType"]
  
    # checking for existing user
    user = User.query\
        .filter_by(email = email)\
        .first()

    users = User.query.all()

    if not user:
        # database ORM object
        user = User(
            public_id = str(uuid.uuid4()),
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            password = generate_password_hash(password),
            date_created=datetime.now(),
            date_modified=datetime.now(),
        )
        if users:
            user.user_type = user_type or "staff"
        else:
            user.user_type = "admin"

        # insert user
        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)



@auth.route('/users', methods=['GET'])
def users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '*', type=str)

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
        .paginate(page=page, per_page=per_page)

    return jsonify(getPaginatedDict(getUsersList(paginated_items.items), paginated_items))

@auth.route('/users/<int:id>', methods=['GET'])
@token_required
def getUserDetails(id):
    return jsonify(getUserDict(User.query.filter_by(id=id).first()))

@auth.route('/users/<int:id>', methods=['PUT'])
@token_required
def updateProductDetails(id):
    email = request.json["email"]
    first_name = request.json["firstName"]
    last_name = request.json["lastName"]
    username = request.json["username"]
    user = User.query.filter_by(id=id).first()

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.username = username
    user.date_modified = datetime.now()

    db.session.commit()

    return "Success", 200

@auth.route('/users/<int:id>', methods=["DELETE"])
def deleteUser(id):
    user = User.query.filter_by(id=id).first()
    if user.sales or user.purchases:
        return "This user can not be deleted because it has sales or purchases connected to it!", 500
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return "Success", 200

@auth.route('/verify-token', methods=['POST'])
@token_required
def verify_token():
    return jsonify({'success': True}), 200

@auth.route('/current-user')
@token_required
def currentUser():
    token = request.headers['x-access-token']
    data = jwt.decode(token, current_app.config['SECRET_KEY'])
    current_user = getUsersList(User.query\
        .filter_by(public_id = data['public_id'])\
        .all())[0]
    return jsonify(current_user)

@auth.route('/users/demo', methods=["GET"])
def createDemoUsers():
    demo = [
        ["eol", "nuha", "eolnuha", "eol@gmail.com", "admin"],
        ["ledri", "nuha", "ledrinuha", "ledri@gmail.com", "staff"],
        ["lela", "nuha", "lelanuha", "lela@gmail.com", "staff"],
        ["edona", "saliu", "edonasaliu", "edona@gmail.com", "staff"],
    ]
    for i in demo:
        db.session.add(User(
            public_id=str(uuid.uuid4()),
            first_name=i[0], 
            last_name=i[1], 
            username=i[2], 
            email=i[3], 
            password=generate_password_hash("kosova22"), 
            user_type=i[4],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            ))
        db.session.commit()
    return "success", 200