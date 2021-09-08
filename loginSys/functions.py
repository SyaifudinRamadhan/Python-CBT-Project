# def cetak():
# 	print("hello worl")
from . import models
from django.shortcuts import render, redirect
from django.contrib.auth import login as loginSys, logout, authenticate

# Fungsi ini mengembalikan text berupa nama dikumen yang dituju
def loginCheck(request, position):
	userlogged = str(request.user)

	if userlogged != 'AnonymousUser': 
		userSec = models.user_second.objects.filter(no_induk = userlogged)

		if position != userSec[0].status:
			if userSec[0].status == 'siswa':
				return '/stdn_auth'

			elif userSec[0].status == 'guru':
				return '/teach_auth'

			else :
				return '/panel'

	else :
		return redirect('/oAuth')

# Fungsi ini mengembalikan text berupa nama dikumen yang dituju
def loginCore(request, no_induk, pwd):
	authen = authenticate(request, username = no_induk, password = pwd)

	print(authen)
	print('\n\n')

	if authen != None:
		loginSys(request, authen)
		print(request.user, authen)
		print('login benar')

		userSec = models.user_second.objects.filter(no_induk = no_induk)
		print(type(userSec[0].status))

		if userSec[0].status == 'siswa':
			print('\nAnda terdaftar sebagai siswa')
			return 'dashboard_siswa.html'		
		elif userSec[0].status == 'guru':
			print('\nAnda terdaftar sebagai Guru')
			return 'dashboard_guru.html'	
		else :
			print('\nAnda terdaftar sebagai admin')
			return 'dashboard_admin.html'	

	else :
		print(request.user)
		print('login salah')

		return 'login.html'