$(document).ready(function($) {

	/* accordion */
	$('#accordion').find('.accordion-toggle').click(function() {
		$(this).next().slideToggle('fast');
		$(".accordion-content").not($(this).next()).slideUp('fast');
	});

	/* add section */
	$('#fill_with_json').click(function (e) {
		e.preventDefault();
		sendAjax('/fill-db-from-json', '', function (answer) {
			alert(answer);
		});
	});

	$('button.order_submit').click(function (e) {
		e.preventDefault();
		var data = $('#add_order').serialize();
		sendAjax('/order-add', data, function (answer) {
			addedOrderData = JSON.parse(answer);
			if (addedOrderData['res'] < 0)
				alert('order was not added');
			else {
				$('tbody').append(getNewRowForTable({
					id: addedOrderData['res'],
					name: 'order',
					colVals: [
						{col: 'product', val: getParamterFromUrlByKeyName(data, 'product')},
						{col: 'count', val: getParamterFromUrlByKeyName(data, 'count')},
						{col: 'orderer', val: getParamterFromUrlByKeyName(data, 'orderer')},
						{col: 'cost', val: addedOrderData['cost']},
						{col: 'terms', val: getParamterFromUrlByKeyName(data, 'terms')}]
				}));
				$('#add_order')[0].reset();
				$('#add_order').parent().css({'display': 'none'});
			}
		});
	});

	$('button.orderer_submit').click(function (e) {
		e.preventDefault();
		var data = $('#add_orderer').serialize();
		sendAjax('/orderer-add', data, function (answer) {
			if (answer < 0)
				alert('orderer was not added');
			else {
				$('tbody').append(getNewRowForTable({
					id: answer,
					name: 'orderer',
					colVals: [
						{col: 'name', val: getParamterFromUrlByKeyName(data, 'name')},
						{col: 'surname', val: getParamterFromUrlByKeyName(data, 'surname')}]
				}));
				$('#add_orderer')[0].reset();
				$('#add_orderer').parent().css({'display': 'none'});
			}
		});
	});

	$('button.department_submit').click(function (e) {
		e.preventDefault();
		var data = $('#add_department').serialize();
		sendAjax('/department-add', data,  function (answer) {
			if (answer < 0)
				alert('department was not added');
			else {
				$('tbody').append(getNewRowForTable({
					id: answer,
					name: 'department',
					colVals: [
						{col: 'department', val: getParamterFromUrlByKeyName(data, 'department')}]
				}));
				$('#add_department')[0].reset();
				$('#add_department').parent().css({'display': 'none'});
			}
		});
	});

	$('button.product_submit').click(function (e) {
		e.preventDefault();
		var data = $('#add_product').serialize();
		sendAjax('/product-add', data, function (answer) {
			if (answer < 0)
				alert('order was not added');
			else {
				$('tbody').append(getNewRowForTable({
					id: answer,
					name: 'product',
					colVals: [
						{col: 'product', val: getParamterFromUrlByKeyName(data, 'product')},
						{col: 'cost', val: getParamterFromUrlByKeyName(data, 'cost')},
						{col: 'department', val: getParamterFromUrlByKeyName(data, 'department')}]
				}));
				$('#add_product')[0].reset();
				$('#add_product').parent().css({'display': 'none'});
			}
		});
	});
	/* end add section */


	/* delete section */
	$('.department-btn-link').click(function (e) {
		e.preventDefault();
		if ($(this).attr('class').indexOf('change') >= 0) {
			setDataToDepartmentUpdateForm($(this));
		}
		else {
			$(this).parent().parent().remove();
			sendAjax('/department-del', 'id=' + $(this).parent().parent().attr('class'), function (answer) {});
		}
	});

	$('.order-btn-link').click(function (e) {
		e.preventDefault();
		if ($(this).attr('class').indexOf('change') >= 0) {
			setDataToOrderUpdateForm($(this));
		}
		else {
			$(this).parent().parent().remove();
			sendAjax('/order-del', 'id=' + $(this).parent().parent().attr('class'), function (answer) {});
		}
	});

	$('.product-btn-link').click(function (e) {
		e.preventDefault();
		if ($(this).attr('class').indexOf('change') >= 0) {
			setDataToProductUpdateForm($(this));
		}
		else {
			$(this).parent().parent().remove();
			sendAjax('/product-del', 'id=' + $(this).parent().parent().attr('class'), function (answer) {});
		}
	});

	$('.orderer-btn-link').click(function (e) {
		e.preventDefault();
		$(this).parent().parent().remove();
		sendAjax('/orderer-del', 'id=' + $(this).parent().parent().attr('class'), function (answer) {});
	});
	/* end delete section */

	/* update section */
	$('button.product_update').click(function (e) {
		e.preventDefault();
		var data = $('#update_product').serialize();
		sendAjax('/product-update', data, function (answer) {
			var id = getParamterFromUrlByKeyName(data, 'id');
			$('.' + id).replaceWith(getNewRowForTable({
				id: id,
				name: 'product',
				colVals: [
					{col: 'product', val: getParamterFromUrlByKeyName(data, 'product')},
					{col: 'cost', val: getParamterFromUrlByKeyName(data, 'cost')},
					{col: 'department', val: $('.' + id + ' > td > .department').text()}]
			}));
			$('#update_product')[0].reset();
			$('#update_product').parent().css({'display': 'none'});
		});
	});

	$('button.order_update').click(function (e) {
		e.preventDefault();
		var data = $('#update_order').serialize();
		sendAjax('/order-update', data, function (answer) {
			var id = getParamterFromUrlByKeyName(data, 'id'),
				cost = $('.' + id + ' > td > .cost').text(),
				oldCount = $('.' + id + ' > td > .count').text(),
				newCount = getParamterFromUrlByKeyName(data, 'product');
			$('.' + id).replaceWith(getNewRowForTable({
				id: id,
				name: 'order',
				colVals: [
					{col: 'product', val: getParamterFromUrlByKeyName(data, 'product')},
					{col: 'count', val: getParamterFromUrlByKeyName(data, 'count')},
					{col: 'orderer', val: $('.' + id + ' > td > .orderer').text()},
					{col: 'cost', val: answer},
					{col: 'terms', val: getParamterFromUrlByKeyName(data, 'terms')}]
			}));
			$('#update_order')[0].reset();
			$('#update_order').parent().css({'display': 'none'});
		});
	});

	$('button.department_update').click(function (e) {
		e.preventDefault();
		var data = $('#update_department').serialize();
		sendAjax('/department-update', data, function (answer) {
			var id = getParamterFromUrlByKeyName(data, 'id');
			$('.' + id).replaceWith(getNewRowForTable({
				id: id,
				name: 'department',
				colVals: [
					{col: 'department', val: getParamterFromUrlByKeyName(data, 'department')}]
			}));
			$('#update_department')[0].reset();
			$('#update_department').parent().css({'display': 'none'});
		});
	});
	/* end update section */

});

function getParamterFromUrlByKeyName(url, name) {
	var sURLVariables = decodeURIComponent(('/' + url).substring(1)).split('&'), sParameterName;

	for (var i = 0; i < sURLVariables.length; i++) {
		sParameterName = sURLVariables[i].split('=');

		if (sParameterName[0] === name)
			return sParameterName[1] === undefined ? true : sParameterName[1];
	}
}

function sendAjax(link, data, callback) {
	$.ajax({
		url: link,
		type: 'get',
		data: data,
		success: callback
	});
}

function setDataToOrderUpdateForm($orderObj) {
	var $orderNumber = $orderObj.parent().parent().attr('class'),
		$order = "." + $orderNumber;
	$('#update_order').parent().slideDown('fast');
	$('#update_order > .product').val($($order + " > td > .product").text());
	$('#update_order > .count').val($($order + " > td > .count").text());
	$('#update_order > .terms').val($($order + " > td > .terms").text());
	$('#update_order').children('.order_id').remove();
	$('#update_order').append('<input name="id" class="order_id" type="hidden" value="' + $orderNumber + '">');
}

function setDataToDepartmentUpdateForm($departmentObj) {
	var $departmentNumber = $departmentObj.parent().parent().attr('class'),
		$department = "." + $departmentNumber;
	$('#update_department').parent().slideDown('fast');
	$('#update_department > .department').val($($department + " > td > .department").text());
	$('#update_department').children('.department_id').remove();
	$('#update_department').append('<input name="id" class="department_id" type="hidden" value="' + $departmentNumber + '">');
}

function setDataToProductUpdateForm($productObj) {
	var $productNumber = $productObj.parent().parent().attr('class'),
		$product = "." + $productNumber;
	$('#update_product').parent().slideDown('fast');
	$('#update_product > .product').val($($product + " > td > .product").text());
	$('#update_product > .cost').val($($product + " > td > .cost").text());
	$('#update_product').children('.product_id').remove();
	$('#update_product').append('<input name="id" class="product_id" type="hidden" value="' + $productNumber + '">');
}

function getNewRowForTable(data) {
	var str = '<tr class="' + data.id + '">';
	for (var i = 0; i < data.colVals.length; i++)
		str += '<td><span class="' + data.colVals[i].col + '">' + data.colVals[i].val + '</span></td>';
	str += '<td><a href="?action=update&id=' + data.id + '" id="update- '+ data.id + '" class="change ' + data.name + '-btn-link">change</a> \
			<a href="?action=delete&id=' + data.id + '" id="delete-' + data.id + '" class="delete ' + data.name + '-btn-link">delete</a></td></tr>';
	return str;

}
