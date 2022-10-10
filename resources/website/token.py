
from functools import wraps
from flask import request, current_app, jsonify
import jwt
from .models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        return  f()
  
    return decorated
    

def currentUser(request):
    token = request.headers["x-access-token"]
    data = jwt.decode(token, current_app.config['SECRET_KEY'])
    return User.query\
        .filter_by(public_id = data['public_id'])\
        .first()