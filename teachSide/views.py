from django.shortcuts import render, redirect, HttpResponse
from loginSys import functions as fn, models as models_user
from adminSide import getData_functions as f_get
from adminSide.pool_admin_tch import data_quest
import json as simplejson
from adminSide import controller as ctrl
import sys
import os

memory = data_quest()
# Create your views here.
def index (request):
	# print('masuk index')
	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		# print('-')
		return redirect(check_logged)

	profile = models_user.user_second.objects.get(no_induk = request.user).profile
	# slc_crs, slc_tch, id_admin = f_get.for_add_quest(request)
	# slc_cls = f_get.get_list_class(request)
	# ---------- Write Code (Logic System) Here ---------------


	# if request.method == "POST" and request.POST.get('add') != None:
	# 	ctrl.add_quest_tbl_0(request)
	# 	return redirect('/panel_sec/create_quest')

	context = {
		'status':'Teacher',
		# 'slc_crs':slc_crs,
		# 'slc_cls':slc_cls,
		# 'id_admin':id_admin,
		'name': models_user.user_second.objects.get(no_induk = request.user).username,
		'profile':profile,
	}

	return render(request, 'teach_panel/dashboard_tch.html', context)
	# return HttpResponse('Hello')

def class_manage (request):
	print('cek masuk')
	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		return redirect(check_logged)

	report = ''
	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
	out1, slc_tch, out2 = f_get.for_add_quest(request, pss='teacher')
	# ---------- Write Code (Logic System) Here ---------------

	if request.method =="POST" and request.POST.get('add_manual') != None:
		err = ctrl.add_class_manual(request, pss='teacher')
		if err == '':
			return redirect('/panel_sec/class_manage')
		else:
			report = err

	if request.method =="POST" and request.POST.get('add_auto') != None:
		err, data = f_get.read_xls_online(request)
		if err == '':
			err = ctrl.add_class_auto(request, data, pss='teacher')
			if err == '':
				return redirect('/panel_sec/class_manage')
			else:
				report = err
		else:
			report = err

	if request.method =="POST" and request.POST.get('edit') != None:
		err = ctrl.edit_class(request, pss='teacher')
		if err == '':
			return redirect('/panel_sec/class_manage')
		else:
			report = err

	if request.method =="POST" and request.POST.get('delete') != None:
		err = ''
		try:
			ctrl.del_class(request)
		except Exception as e:
			err = e
		if err == '':
			return redirect('/panel_sec/class_manage')
		else:
			report = err
			print('cek error : ',report)

	view = f_get.get_list_class(request, pss='teacher')

	context={
		'main':obj_user_main,
		'second':obj_user_second,
		'list':view,
		'tch_list':slc_tch,
		'report':report,
	}

	return render(request, 'teach_panel/class_page.html', context)

# def tch_manage (request):

# 	check_logged = fn.loginCheck(request, state = 'guru')
# 	if check_logged != 'None':
# 		return redirect(check_logged)

# 	report = ''
# 	obj_user_main, obj_user_second = f_get.getDataAdmin(request)

# 	# ---------- Write Code (Logic System) Here ---------------

# 	if request.method == "POST" and request.POST.get('add_manual') != None:
# 		msg = fn.add_acc_manual
# 		print(len(msg),'cek')
# 		if len(msg) == 0:
# 			return redirect('/panel_sec/teacher_mng')
# 		else:
# 			report = msg

# 	if request.method == "POST" and request.POST.get('add_auto') != None:
# 		msg, list_data = f_get.read_xls_online(request)
# 		if msg == '':
# 			msg, err = fn.add_acc_auto(request, list_data)
# 			if err == '':
# 				return redirect('/panel_sec/teacher_mng')
# 			else :
# 				report = err
# 		else:
# 			report = msg

# 	if request.method == "POST" and request.POST.get('edit') != None:
# 		msg = fn.editStdAcc(request, pss='teacher', use='multi')
# 		if len(msg) == 0:
# 			return redirect('/panel_sec/teacher_mng')
# 		else:
# 			report = msg

# 	if request.method == "POST" and request.POST.get('delete') != None:
# 		msg = ctrl.del_tch_stdn(request)
# 		if msg == '':
# 			return redirect('/panel_sec/teacher_mng')
# 		else:
# 			report = msg

# 	view = f_get.view_tch_data(request)

# 	context={
# 		'main':obj_user_main,
# 		'second':obj_user_second,
# 		'list':view,
# 		'report':report,
# 	}

# 	return render(request, 'teacher_mng_page.html', context)

def stdn_manage (request):

	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		return redirect(check_logged)

	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
	report = ''
	# ---------- Write Code (Logic System) Here ---------------
	if request.method =="POST" and request.POST.get('add_manual') != None:
		msg = fn.add_acc_manual(request, add_for='student')
		if len(msg) == 0:
			return redirect('/panel_sec/stdn_manage')
		else :
			report = msg

	if request.method == "POST" and request.POST.get('edit') != None:
		msg = fn.editStdAcc(request, use='multi')
		if len(msg) == 0:
			return redirect('/panel_sec/stdn_manage')
		else:
			report = msg

	if request.method == "POST" and request.POST.get('add_auto') != None:
		msg, data_list = f_get.read_xls_online(request)
		if msg == '':
			msg, err = fn.add_acc_auto(request, data_list, add_for='student', pss='teacher')
			if err == '':
				return redirect('/panel_sec/stdn_manage')
			else:
				report = err
		else:
			report = msg

	if request.method == "POST" and request.POST.get('delete') != None:
		msg = ctrl.del_tch_stdn(request, del_for='student')
		if msg == '':
			return redirect('/panel_sec/stdn_manage')
		else:
			report = msg

	view = f_get.view_stdn_data(request, pss='teacher')
	tch_list = f_get.view_tch_data(request, pss='teacher')
	class_list = f_get.get_list_class(request, pss='teacher', for_='select')
 	# print(view)
	context={
		'main':obj_user_main,
		'second':obj_user_second,
		'list':view,
		'tch_list':tch_list,
		'class_list':class_list,
		'report':report,
	}

	return render(request, 'teach_panel/stdn_mng_page.html', context)

def course_manage (request):

	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		return redirect(check_logged)

	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
	report = ''
	# ---------- Write Code (Logic System) Here ---------------

	if request.method == "POST" and request.POST.get('add_manual') != None:
		err = ctrl.add_crs_manual(request, pss='teacher')
		if err == '':
			return redirect('/panel_sec/course_mng')
		else:
			report = err

	if request.method == "POST" and request.POST.get('add_auto') != None:
		msg, data = f_get.read_xls_online(request)
		if msg == '':
			msg = ctrl.add_crs_auto(request, data, pss='teacher')
			if msg == '':
				return redirect('/panel_sec/course_mng')
			else:
				report = msg
		else:
			report = msg

	if request.method == "POST" and request.POST.get('edit') != None:
		msg = ctrl.edit_crs(request, pss='teacher')
		if msg == '':
			return redirect('/panel_sec/course_mng')
		else:
			report = msg

	if request.method == "POST" and request.POST.get('delete') != None:
		err = ''
		try:
			ctrl.del_course(request)
		except Exception as e:
			print(e)

		if err == '':
			return redirect('/panel_sec/course_mng')
		else:
			report = err

	view, tch_list, tmp2 = f_get.for_add_quest(request, pss='teacher')

	context={
			'main':obj_user_main,
			'second':obj_user_second,
			'list':view,
			'tch_list':tch_list,
			# 'class_list':class_list,
			'report':report,
		}

	return render(request, 'teach_panel/course_page.html', context)

def quest_basic (request):

	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		return redirect(check_logged)
	
	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
	# Membersihkan memory object saat memuat halaman ini
	memory.clear_list()
	# ---------- Write Code (Logic System) Here ---------------
	view = f_get.get_quest_table(request, pss='teacher')
	slc_crs, slc_tch, id_admin = f_get.for_add_quest(request, pss='teacher')
	slc_cls = f_get.get_list_class(request, pss='teacher', for_='select')
	
	if request.method == "POST" and request.POST.get('add') != None:
		ctrl.add_quest_tbl_0(request)
		return redirect('/panel_sec/create_quest')

	if request.method == "POST" and request.POST.get('add_auto') != None:
		# 1. read file xls online langsung
		err, xls_data = f_get.read_xls_online(request)
		del xls_data[0]
		if err == '':
			# 2. membuat data di db terkait datasoal ini
			ctrl.add_quest_tbl_0(request)
			# 3. Mengkomparasi file gambar uploadan dengan yang ada di list dari xls
			data = ctrl.compare_file_in_xls(request, xls_data)
			# 4. Merubah list menjadi xls
			file_name = ctrl.create_xls(request, data)
			# 5. Memasukkan nama file xls ke dalam db yang serialnya '-'
			err = ctrl.add_quest_tbl_1(request, file_name, pss='teacher')
			return redirect('/panel_sec/quest_data')
		print(err,' - jika error\n')

	if request.method == "POST" and request.POST.get('edit_auto') != None:
		err, xls_data = f_get.read_xls_online(request)
		del xls_data[0]
		# 1. read file xls online langsung
		if err == '':
			# 2. Mengkomparasi file gambar uploadan dengan yang ada di list dari xls
			data = ctrl.compare_file_in_xls(request, xls_data)
			# 3. Merubah list menjadi xls
			file_name = ctrl.create_xls(request, data)
			# 4. Memasukkan nama file xls ke dalam db yang serialnya '-'
			err = ctrl.add_quest_tbl_1(request, file_name, pss='teacher',serial_quest = request.POST.get('name_data'))
			os.remove('media/'+str(request.POST.get('name_data')))
			return redirect('/panel_sec/quest_data')
		print(err,' - jika error\n')

	if request.GET.get('del') != None:
		data, file_name = f_get.read_xls_storage(request, request.GET.get('del'))
		# print(file_name,' --- file_name---\n')
		if file_name == '':
			return redirect('/panel_sec/quest_data')
		else :
			ctrl.delete_for_quest(request, data, file_name)
			return redirect('/panel_sec/quest_data')

	if request.GET.get('id') != None:
		data, file_name = f_get.read_xls_storage(request, request.GET.get('id'))
		memory.set_data_quest(data, file_name)
		
		if memory.get_len_data() != 0 or file_name != '':
			return redirect('/panel_sec/edit_quest')
		else:
			memory.clear_list()
			return redirect('/panel_sec/quest_data')


	context = {
		'data':view,
		'slc_tch':slc_tch,
		'slc_crs':slc_crs,
		'slc_cls':slc_cls,
		'id_admin':id_admin,
		'main':obj_user_main,
		'second':obj_user_second,
	}

	return render(request, 'teach_panel/quest_list.html', context)

def quest_edit (request):

	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		return redirect(check_logged)

	if memory.get_len_data() == 0:
		return redirect('/panel_sec/quest_data')

	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
	# handilng refresh page agar datanya tidak kosong di formnya
	print(memory.get_all_data(),'\n')
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
			return redirect('/panel_sec/create_quest')
		else:
			print('Data yang dihapus belum ada\n')

	# Untuk menyimpan file baru stelah di edit
	if request.method == "POST" and request.POST.get('finish') != None:
		memory.next(request)
		file = ctrl.create_xls(request, memory.get_all_data())
		err = ctrl.add_quest_tbl_1(request, file, pss='teacher',serial_quest = memory.get_last_file_name())
		memory.clear_list()
		print(err,'\n')
		return redirect('/panel_sec/quest_data')


	context = {
		'index_params':index_params,
		'numbering':index_params+1,
		'len_data':len_data,
		'view':simplejson.dumps(view),
		'len_view':len(view),
		'view_n':view,
		'main':obj_user_main,
		'second':obj_user_second,
	}

	return render(request, 'teach_panel/add_quest.html', context)

def quest_add (request):

	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		return redirect(check_logged)

	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
	# handilng refresh page agar datanya tidak kosong di formnya
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
			return redirect('/panel_sec/create_quest')
		else:
			print('Data yang dihapus belum ada\n')

	if request.method == "POST" and request.POST.get('finish') != None:
		memory.next(request)
		file = ctrl.create_xls(request, memory.get_all_data())
		err = ctrl.add_quest_tbl_1(request, file, pss='teacher')
		memory.clear_list()
		return redirect('/panel_sec/quest_data')


	context = {
		'index_params':index_params,
		'numbering':index_params+1,
		'len_data':len_data,
		'view':simplejson.dumps(view),
		'len_view':len(view),
		'view_n':view,
		'main':obj_user_main,
		'second':obj_user_second,
	}

	return render(request, 'teach_panel/add_quest.html', context)

def schdl_manage (request):

	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		return redirect(check_logged)

	report = ''
	# ---------- Write Code (Logic System) Here ---------------
	
	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
	schedule = f_get.getSchedule(request,'',teach = True, students=False)

	context={
		'main':obj_user_main,
		'second':obj_user_second,
		'schedule':schedule,
		# 'slc_tch':slc_tch,
		# 'slc_crs':slc_crs,
		# 'slc_class':slc_class,
		'report':report,
	}

	return render(request, 'teach_panel/schedule_admin.html', context)

# def activate (request):

# 	check_logged = fn.loginCheck(request, state = 'admin')
# 	if check_logged != 'None':
# 		return redirect(check_logged)

# 	# ---------- Write Code (Logic System) Here ---------------
# 	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
# 	schedule = f_get.getSchedule(request,'',admin = True, students=False)

# 	if request.method == "POST" and request.POST.get('activate') != None:
# 		ctrl.set_active(request)
# 		return redirect('/panel_sec/set_test_active')

# 	if request.method == "POST" and request.POST.get('deactivate') != None:
# 		ctrl.set_deactive(request)
# 		return redirect('/panel_sec/set_test_active')

# 	context={
# 		'main':obj_user_main,
# 		'second':obj_user_second,
# 		'schedule':schedule,
# 	}

# 	return render(request, 'test_manage_page.html', context)

def my_acc (request):

	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		return redirect(check_logged)

	# ---------- Write Code (Logic System) Here ---------------
	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
	spec = models_user.theachers_user.objects.get(no_induk = request.user)
	admin_list = models_user.user_second.objects.filter(status = 'admin')
	confirm = []
	if request.method == "POST" and request.POST.get('edit') != None:
		confirm = fn.editStdAcc(request, pss = 'teacher')
		if len(confirm)	== 0:
			return redirect('/panel_sec/set_my_acc') 	

	context={
		'main':obj_user_main,
		'second':obj_user_second,
		'third':spec,
		'admin_slc':admin_list,
		'confirm':confirm,
		'len_confirm':len(confirm),
	}
	
	return render(request, 'teach_panel/my_acc_admin.html', context)

def result_test_view(request):
	check_logged = fn.loginCheck(request, state = 'guru')
	if check_logged != 'None':
		return redirect(check_logged)
	msg = ''
	# ---------- Write Code (Logic System) Here ---------------
	if request.method =="POST" and request.POST.get('delete') != None:
		try:
			ctrl.del_result_test(request)
			return redirect('/panel_sec/view_res_test')
		except Exception as e:
			msg = 'Data gagal dihapus'

	obj_user_main, obj_user_second = f_get.getDataAdmin(request)
	view = f_get.viewResultTest (request, request.user, teach=True, students=False)

	context={
		'main':obj_user_main,
		'second':obj_user_second,
		'msg':msg,
		# 'confirm':confirm,
		# 'len_confirm':len(confirm),
		'list_res': view,
	}
	
	return render(request, 'teach_panel/view_res_test.html', context)




