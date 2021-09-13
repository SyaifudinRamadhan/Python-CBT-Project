from django.shortcuts import render, redirect
from django.contrib.auth import login as loginSys, logout, authenticate
from loginSys import functions, models
from adminSide import models as models_2, getData_functions as f_get
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from . import controller_test as C_T

# Halaman depan (Umum)
def index (request):
	
	return render(request, 'index.html')


# Semua di bawah halaman setelah login
def dashboard (request):
	# Cek kondisi login user
	nextStep = functions.loginCheck(request)

	if nextStep != 'None' :
		return redirect(nextStep)

	state = functions.getState(request.user)
	name = functions.getName(request.user)

	context = {
		'status':state,
		'name':name,
	}

	return render(request, 'dashboard_siswa.html', context)

def schedule (request):
	# Cek kondisi login user
	nextStep = functions.loginCheck(request)

	if nextStep != 'None' :
		return redirect(nextStep)

	page = request.GET.get('page')
	print('cek saja \n',page,'\n')

	listSchedule = f_get.getSchedule(request, request.user)
	lisRes = []
	view = []

	for x in range(len(listSchedule)):
		date = listSchedule[x].date
		time = listSchedule[x].start
		state = listSchedule[x].state
		token = listSchedule[x].token
		course = models_2.course_data.objects.filter(id = listSchedule[x].id_course)
		class_ = models_2.class_data.objects.filter(id = listSchedule[x].id_course)

		tmp = [date, time, state, course[0].course_name, class_[0].class_name, token]
		lisRes.append(tmp)

	paginate = Paginator(lisRes, 10)
	print(paginate.page(1))

	try:
		view = paginate.page(page)
	except PageNotAnInteger:
		view = paginate.page(1)
	except EmptyPage:
		view = paginate.page(paginate.num_pages)

	context = {
		'name':functions.getName(request.user),
		'schedule_list':lisRes,
		'count':len(listSchedule),
		'data':view,
	}

	return render(request, 'schedule_list.html', context)

def startTest (request):
	# Cek kondisi login user
	nextStep = functions.loginCheck(request)

	if nextStep != 'None' :
		return redirect(nextStep)

	context = {
		'name':functions.getName(request.user)
	}

	return render(request, 'start_test.html', context)

def viewResTest (request):
	# Cek kondisi login user
	nextStep = functions.loginCheck(request)

	if nextStep != 'None' :
		return redirect(nextStep)
	page = request.GET.get('page')
	print('\n',page,'\n')



	listData = []
	view = []
	res = f_get.viewResultTest(request, request.user)
	for tmp in range(len(res)):
		date = res[x].date
		result = res[x].result
		tmp = models_2.quest_data.objects.filter(res[x].id_course)
		course = models_2.course_data.objects.filter(id = tmp[0].id_course)
		id_teach = res[x].id_teacher
		tmp2 = [date, course, id_teach, result]
		listData.append(tmp2)

	paginate = Paginator(listData, 10)

	try:
		view = paginate.page(page)
	except PageNotAnInteger :
		view = paginate.page(1)
	except EmptyPage :
		view = paginate.page(paginate.num_pages)

	context = {
		'name':functions.getName(request.user),
		'data': view,
		'count': len(res),
	}

	return render(request, 'result_test_list.html', context)

def evaluationView (request):
	# Cek kondisi login user
	nextStep = functions.loginCheck(request)

	if nextStep != 'None' :
		return redirect(nextStep)

	context = {
		'name':functions.getName(request.user)
	}

	return render(request, 'view_evaluation.html', context)

def setAccount (request):
	# Cek kondisi login user
	nextStep = functions.loginCheck(request)
	confirm = []

	if nextStep != 'None' :
		return redirect(nextStep)

	if request.method == "POST":
		confirm = functions.editStdAcc(request)

	main = User.objects.filter(username = request.user)
	spec = models.students_user.objects.filter(no_induk = request.user)
	second = models.user_second.objects.filter(no_induk = request.user)
	arr = ['dds','fdfdf','fdghfg']

	context = {
		'name':functions.getName(request.user),
		'mainUser': main[0],
		'std_user': spec[0],
		'sec_user': second[0],
		'confirm' : confirm,
		'profile' : "/media/"+second[0].profile,
	}

	print(main[0].username)

	return render(request, 'set_acc.html', context)

def testMain (request):
	# Cek kondisi login user
	nextStep = functions.loginCheck(request)

	if nextStep != 'None' :
		return redirect(nextStep)

	# C_T.run_test()
	directory, inf = f_get.getQuestFile(request)

	dic_quest = ''
	err_msg = ''
	second = models.user_second.objects.filter(no_induk = request.user)

	context = {
		'name':functions.getName(request.user),
		'profile' : "/media/"+second[0].profile,
	}

	if inf == '' :
		print(directory,'\n')
		# Mengambil data untuk di ditampilkan
		dic_quest, keys, err_msg = C_T.run_test(directory)
		if err_msg == True :
			context = {
				'name':functions.getName(request.user),
				'confirm': '',
				'text_quest' : dic_quest['text_quest'],
				'ans_txt' : dic_quest['ans_txt'],
				'val_ans' : dic_quest['val_ans'],
				'type_quest' : dic_quest['type_quest'],
				'max_check' : dic_quest['max_check'],
				'img_quest' : dic_quest['img_quest'],
				'videos_quest' : dic_quest['videos_quest'],
				'audio_quest' : dic_quest['audio_quest'],
				'profile' : "/media/"+second[0].profile,
			}
		elif err_msg == False :
			context = {
				'name':functions.getName(request.user),
				'confirm':inf+" Error soal RUSAK",
				'profile' : "/media/"+second[0].profile,
			}
			# jika masuk sini harus di return render page lain
			return render(request,'test_confirm.html', context)
	else :
		context = {
			'name':functions.getName(request.user),
			'confirm':inf,
			'profile' : "/media/"+second[0].profile,
		}
		# jika masuk sini harus di return render page lain
		return render(request,'test_confirm.html', context)

	print(err_msg,' ',inf,' ',context,'\n')
	return render(request, 'test_main.html', context)
