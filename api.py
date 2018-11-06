from flask import Flask
from flask_restful import Resource, Api, reqparse
from rates import OER
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from config import DB_URI

parser = reqparse.RequestParser()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)
api = Api(app)

class Stats(db.Model):
	__tablename__ = 'Currency Stats'
	id = db.Column(db.Integer, primary_key=True)
	currency = db.Column(db.String(3), nullable=False)
	amount = db.Column(db.Numeric(20,8))
	rate = db.Column(db.Numeric(20,8))
	finalAmount = db.Column(db.Numeric(20,8))

class GrabAndSave(Resource):

	def post(self):
		parser.add_argument('amount', type=float, help='Amount ex-4.012')
		parser.add_argument('currency', type=str, help='ISO3 code, ex-BTC,USD')
		args = parser.parse_args(strict=True)
		try:
			amount = args['amount']
			currency = args['currency']
			rate = OER().getRate(currency)
			finalAmount = rate * amount

			row = Stats(currency=currency,
						amount=amount,
						rate=rate,
						finalAmount=finalAmount)
			db.session.add(row)
			db.session.commit()
			resp = jsonify(success=True)
			return resp
		except Exception as e:
			data = { 'error':True,  'message':str(e)}
			resp = jsonify(data)
			return resp

class Last(Resource):

	def get(self):
		parser.add_argument('currency', type=str, help="'ISO3 code, ex-BTC,USD'")
		parser.add_argument('number', type=int, help="Number of results in int, ex- 3")
		args = parser.parse_args(strict=True)
		currency = args['currency']
		number = args['number']
		result = []
		try:
			if currency and number:
				rows = Stats.query.filter_by(currency=currency).order_by(Stats.id.desc()).limit(number)
				for row in rows:
					result.append(self._getFormattedRow(row))
			elif currency:
				row = Stats.query.filter_by(currency=currency).order_by(Stats.id.desc()).first()
				result.append(self._getFormattedRow(row))
			elif number:
				rows = Stats.query.order_by(Stats.id.desc()).limit(number)
				for row in rows:
					result.append(self._getFormattedRow(row))
			else:
				row = Stats.query.order_by(Stats.id.desc()).first()
				result.append(self._getFormattedRow(row))
			resp = jsonify(result=result)
			return resp
		except Exception as e:
			data = { 'error':True,  'message':str(e)}
			resp = jsonify(data)
			return resp


	def _getFormattedRow(self,row):
		return [row.currency, str(row.amount), str(row.rate), str(row.finalAmount)]
		

api.add_resource(GrabAndSave, '/grab_and_save')
api.add_resource(Last, '/last')

if __name__ == '__main__':
	app.run(debug=True)