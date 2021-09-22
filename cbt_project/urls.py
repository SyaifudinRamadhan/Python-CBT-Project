"""cbt_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'home'),
    path('stdn_auth', views.dashboard, name = 'index'),
    path('schedule_list', views.schedule, name = 'schedule'),
    path('start_test', views.startTest, name = 's_test'),
    path('view_result_test', views.viewResTest, name = 'v_val'),
    path('set_acc', views.setAccount, name = 'my_acc'),
    path('evaluation_view', views.evaluationView, name = 'eval'),
    path('std_test_run', views.testMain, name = 'testrun'),
    path('oAuth/', include(('loginSys.urls','loginSys'), namespace = 'login')),
    path('panel/', include(('adminSide.urls', 'adminSide'), namespace = 'panel_admin')),
    path('cek', views.cek),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)