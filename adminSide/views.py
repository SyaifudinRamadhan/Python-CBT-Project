from django.shortcuts import render, redirect
from loginSys import functions as fn, models as models_user
from . import getData_functions as f_get
from .pool_admin_tch import data_quest
import json as simplejson
from . import controller as ctrl
import sys

memory = data_quest()
# Create your views here.
def index (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------

	context = {
		'status':'Admin',
		'name': models_user.user_second.objects.get(no_induk = request.user).username
	}

	return render(request, 'dashboard_admin.html', context)

def class_manage (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------

	return render(request, 'class_page.html')

def tch_manage (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------

	return render(request, 'teacher_mng_page.html')

def stdn_manage (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------

	return render(request, 'stdn_mng_page.html')

def course_manage (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------

	return render(request, 'course_page.html')

def quest_basic (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------
	view = f_get.get_quest_table(request)
	slc_crs, slc_tch, id_admin = f_get.for_add_quest(request)
	
	if request.method == "POST" and request.POST.get('add') != None:
		ctrl.add_quest_tbl_0(request)
		return redirect('/panel/create_quest')

	if request.method == "POST" and request.POST.get('add_auto') != None:
		# 1. read file xls online langsung
		err, xls_data = f_get.read_xls_online(request)
		if err == '':
			# 2. membuat data di db terkait datasoal ini
			ctrl.add_quest_tbl_0(request)
			# 3. Mengkomparasi file gambar uploadan dengan yang ada di list dari xls
			data = ctrl.compare_file_in_xls(request, xls_data)
			# 4. Merubah list menjadi xls
			file_name = ctrl.create_xls(request, data)
			# 5. Memasukkan nama file xls ke dalam db yang serialnya '-'
			err = ctrl.add_quest_tbl_1(request, file_name)
			return redirect('/panel/quest_data')
		print(err,' - jika error\n')

	context = {
		'data':view,
		'slc_tch':slc_tch,
		'slc_crs':slc_crs,
		'id_admin':id_admin,
	}

	return render(request, 'quest_list.html', context)

def quest_edit (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------

	return render(request, 'edit_quest.html')

def quest_add (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	index_params = memory.get_index_params()
	len_data = memory.get_len_data()
	view = []
	if index_params < len_data :
		print(len_data,'\n')
		view = memory.get_in_page(index_params)

	# ---------- Write Code (Logic System) Here ---------------
	if request.method == "POST" and request.POST.get('next') != None:
		index_params, len_data =  memory.next(request)
		if index_params < len_data:
			view = memory.get_in_page(index_params)
		else:
			print('Data yang dituju belum ada\n')
	if request.method == "POST" and request.POST.get('back') != None:
		index_params, len_data = memory.prev(request)
		if index_params < len_data:
			view = memory.get_in_page(index_params)
		else:
			print('Data yang dituju belum ada\n')

	if request.method == "POST" and request.POST.get('del') != None:
		print(index_params,' ',len_data,'\n')
		if index_params < len_data:
			memory.del_data_quest(index_params)
			return redirect('/panel/create_quest')
		else:
			print('Data yang dihapus belum ada\n')

	if request.method == "POST" and request.POST.get('finish') != None:
		memory.next(request)
		file = ctrl.create_xls(request, memory.get_all_data())
		err = ctrl.add_quest_tbl_1(request, file)
		memory.clear_list()
		return redirect('/panel/quest_data')


	context = {
		'index_params':index_params,
		'numbering':index_params+1,
		'len_data':len_data,
		'view':simplejson.dumps(view),
		'len_view':len(view),
		'view_n':view,
	}

	return render(request, 'add_quest.html', context)

def schdl_manage (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------

	return render(request, 'schedule_admin.html')

def activate (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------

	return render(request, 'test_manage_page.html')

def my_acc (request):

	check_logged = fn.loginCheck(request, state = 'admin')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------

	return render(request, 'my_acc_admin.html')








