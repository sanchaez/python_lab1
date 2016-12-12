from django.shortcuts import render

class View:

	template = ''
	request = None
	data = {}

	def __init__(self, tpl, req, data):
		self.template = tpl
		self.request = req	
		self.data['table'] = data

	def renderPage(self):
		return render(self.request, self.template, self.data)
