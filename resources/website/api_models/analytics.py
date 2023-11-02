from flask_restx import fields

from .. import swagger

percentage_dictionary = swagger.model('SalesInfoDictionary', {
	'chartName': fields.String,
	'currTotal': fields.Float,
	'percentageDiff': fields.Float,
	'prevTotal': fields.Float,
})

chart_dictionary = swagger.model('PurchaseInfoDictionary', {
	'chartName': fields.String,
	'currTotal': fields.Float,
})

gross_net_dictionary = swagger.model('SalesInfoDictionary', {
	'chartName': fields.String,
	'currTotal': fields.Float,
	'grossTotal': fields.Float,
	'netTotal': fields.Float,
})

series_dictionary = swagger.model('SalesSeriesDictionary', {
	'name': fields.String,
	'data': fields.List(fields.Float),
})

percentage_model = swagger.model('Percentage', {
	'info': fields.Nested(percentage_dictionary),
	'options': fields.List(fields.String),
	'series': fields.List(fields.Nested(series_dictionary))
})

gross_net_model = swagger.model('GrossNet', {
	'info': fields.Nested(gross_net_dictionary),
	'options': fields.List(fields.String),
	'series': fields.List(fields.Nested(series_dictionary))
})

chart_model = swagger.model('Chart', {
	'info': fields.Nested(chart_dictionary),
	'options': fields.List(fields.String),
	'series': fields.List(fields.Nested(series_dictionary))
})