
from functools import wraps
from flask import request, current_app, jsonify
import jwt
from .models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
  
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        return  f(*args, **kwargs)
  
    return decorated
    

def currentUser(request):
    token = request.headers["x-access-token"]
    data = jwt.decode(token, current_app.config['SECRET_KEY'])
    return User.query\
        .filter_by(public_id = data['public_id'])\
        .first()