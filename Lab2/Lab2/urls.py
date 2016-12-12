from django.conf.urls import url
from . import controllers

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^order-add', controllers.orderAdd),
    url(r'^department-add', controllers.departmentAdd),
    url(r'^orderer-add', controllers.ordererAdd),
    url(r'^product-add', controllers.productAdd),
    url(r'^fill-db-from-json', controllers.fillDataBaseFromJSON),

    url(r'^order-update', controllers.orderUpdate),
    url(r'^department-update', controllers.departmentUpdate),
    url(r'^product-update', controllers.productUpdate),

    url(r'^order-del', controllers.orderDelete),
    url(r'^department-del', controllers.departmentDelete),
    url(r'^orderer-del', controllers.ordererDelete),
    url(r'^product-del', controllers.productDelete),

    url(r'^orders', controllers.orders),
    url(r'^orderers', controllers.orderers),
    url(r'^products', controllers.products),
    url(r'^departments', controllers.departments),
    url(r'^$', controllers.index)
]
