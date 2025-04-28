"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings

from core.views import payment, process_printing, upload_document,template_list,select_terminal,pay_and_print
from core.views import upload_and_read_files, load_document,detail,update_terminal
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path("upload/<int:pk>/", upload_and_read_files, name="upload_document"),
    path('detail/<int:pk>', detail, name='detail'),
    path("payment/<int:doc_id>/", payment, name="payment"),
    path("print_document/<int:doc_id>",process_printing , name="print_document"),
    path('upload/', upload_and_read_files, name='upload_and_read_files'),
    path('api/update_terminal/<int:terminal_id>/', update_terminal, name='update_terminal'),
    
    path('template_list/', template_list, name="template_list"),
    path('select_terminal/<int:document_id>/', select_terminal, name="select_terminal"),
    path('pay_and_print/<int:document_id>/<int:terminal_id>/', pay_and_print, name="pay_and_print")
    
     
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
