from flask_restx import fields

from .. import swagger

pagination = swagger.model('Pagination', {
    'page': fields.Integer,
    'per_page': fields.Integer,
    'pages': fields.Integer,
    'total': fields.Integer,
    'data': fields.List(fields.Raw),
    'items': fields.Integer,
    'prev_num': fields.String,
    'next_num': fields.String,
    'has_next': fields.Boolean,
    'has_prev': fields.Boolean,
		'page_range': fields.List(fields.Raw),
})
