from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name = 'index_admin'),
	path('class_manage', views.class_manage, name = 'class_data'),
	path('teacher_mng', views.tch_manage, name = 'teacher_data'),
	path('stdn_manage', views.stdn_manage, name = 'stdn_data'),
	path('course_mng', views.course_manage, name = 'course_data'),
	path('quest_data', views.quest_basic, name = 'quest_data_list'),
	# Halaman sekunder untuk kelola soal
	path('edit_quest', views.quest_edit, name = 'edit_quest_data'),
	path('create_quest', views.quest_add, name = 'add_quest'),
	# ---------------------------------
	path('schedule_data', views.schdl_manage, name = 'schedule'),
	path('set_test_active', views.activate, name = 'schedule_set'),
	path('set_my_acc', views.my_acc, name = 'my_acc_admin'),
	path('view_res_test', views.result_test_view, name = 'view_res'),
]