def getOrdersForms():
	return [{
				'name':   'add_order',
				'action': 'add',
				'button': 'order_submit',
				'inputs': [
					{'name': 'product', 'placeholder': 'Product name'},
					{'name': 'count', 'placeholder': 'Count of products'},
					{'name': 'orderer', 'placeholder': 'Orderer: Name Surname'},
					{'name': 'terms', 'placeholder': 'Performance line'}]},
			{
				'name':   'update_order',
				'action': 'update',
				'button': 'order_update',
				'inputs': [
					{'name': 'product', 'placeholder': 'Product name'},
					{'name': 'count', 'placeholder': 'Count of products'},
					{'name': 'terms', 'placeholder': 'Performance line'}]}]

def getDepartmentsForms():
	return [{
				'name':   'add_department',
				'action': 'add',
				'button': 'department_submit',
				'inputs': [
					{'name': 'department', 'placeholder': 'department name'}]},
			{
				'name':   'update_department',
				'action': 'update',
				'button': 'department_update',
				'inputs': [
					{'name': 'department', 'placeholder': 'department name'}]}]

def getOrderersForms():
	return [{
			'name':   'add_orderer',
			'action': 'add',
			'button': 'orderer_submit',
			'inputs': [
				{'name': 'name', 'placeholder': 'Name'},
				{'name': 'surname', 'placeholder': 'Surname'}]}]

def getProductsForms():
	return [{
				'name':   'add_product',
				'action': 'add',
				'button': 'product_submit',
				'inputs': [
					{'name': 'product', 'placeholder': 'Product name'},
					{'name': 'cost', 'placeholder': 'Product cost'},
					{'name': 'department', 'placeholder': 'Product department'}]},
			{
				'name':   'update_product',
				'action': 'update',
				'button': 'product_update',
				'inputs': [
					{'name': 'product', 'placeholder': 'Product name'},
					{'name': 'cost', 'placeholder': 'Product cost'}]}]