import requests
from config import APP_KEY, BASE_URL


class OER(object):

	def __init__(self, base=None, symbols=None, prettyprint=None, show_alternative=None):
		self.base = base
		self.symbols = symbols
		self.prettyprint = prettyprint
		self.show_alternative = show_alternative

	def _get_params(self):
		params = {}
		if self.base:
			params['base'] = self.base
		if self.symbols:
			params['symbols'] = self.symbols
		if self.prettyprint:
			params['prettyprint'] = self.prettyprint
		if self.show_alternative:
			params['show_alternative'] = self.show_alternative
		params['app_id'] = APP_KEY
		return params

	def getRate(self, currency):
		response = requests.get(BASE_URL, params=self._get_params())
		data = response.json()
		rate = data['rates'][currency]
		return rate


if __name__ == '__main__':
	oer = OER()
	rate = oer.getRate('EUR')
	print(rate)






