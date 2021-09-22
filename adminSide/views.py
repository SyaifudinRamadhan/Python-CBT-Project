from django.shortcuts import render, redirect
from loginSys import functions as fn, models as models_user

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

	return render(request, 'quest_list.html')

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

	# ---------- Write Code (Logic System) Here ---------------

	return render(request, 'add_quest.html')

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








