from django.urls import path
from . import views
from .views import document_groups

urlpatterns = [
     path('', views.printer_list, name='printer_list'),
     path("document_tree",views.document_tree,name='document_tree'),
     path('documents/', document_groups, name='document_groups'),
     path('documents/<int:group_id>/', document_groups, name='document_groups'),
     path('print2/<int:document_id>/', views.print_document, name='print_document2'),

    # path('', views.index, name='index'),
    # path('upload/', views.upload_document, name='upload_document'),
    # path('aa/', views.server, name='server'),
    # path('documents/', views.document_list, name='document_list'),
]
