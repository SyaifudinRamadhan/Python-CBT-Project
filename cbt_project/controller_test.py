import random as rd
import pandas as pd

def answear_view_process (data) :
	answear_txt = []
	value_ans_btn = []
	for i in range(len(data)) :
		# ----------------------- Tahapan pengacakan dan penomoran jawaban ------------------------
		tmp = []
		j_s = 6
		for j in range(1,6) :
			t = []
			num = str(j)
			if pd.isna(data[i][j_s]) != True or pd.isna(data[i][j_s+1]) != True :
				if pd.isna(data[i][j_s]) == True :
					t.append('')
					t.append(num+'^`@`^'+data[i][j_s+1])
					# print('masuk 1.0')
				elif pd.isna(data[i][j_s+1]) == True :
					t.append(num+'^`@`^'+data[i][j_s])
					t.append('')
					# print('masuk 1.1')
				else:
					t.append(num+'^`@`^'+data[i][j_s])
					t.append(num+'^`@`^'+data[i][j_s+1])
					# print('masuk 1.2')
			else :
				t.append('')
				t.append('')
				# print('masuk 2')
			j_s += 2
			tmp.append(t)
	
		if data[i][20] == 'Y' :
			rd.shuffle(tmp)
			# print('\n','Ans acak','\n')
		# print('\n',tmp,'\n')
		# -----------------------------------------------------------------------------------------
		
		# -- Pemisahan jawaban dan penomoran sesuai urutan menjadi value button dan label jawaban ---
		
		ans_txt = []
		val_ans = []
		# Untuk ans_txt adalah list berjumlah 5x2
		# Untuk val_ans adalah list berjumlah 5x1
		for k in range(len(tmp)) :
			# NB : 0 adalah milik text jawaban
			#      1 adalah milik gambar jawaban
			if tmp[k][0] == '' and tmp[k][1] == '' :
				ans_txt.append('')
				ans_txt.append('')
				val_ans.append('')
			elif tmp[k][0] != '' and tmp[k][1] == '' :
				# Hasil divid index 0 = value index 1 = text
				divid_0 = tmp[k][0].split('^`@`^')
				
				ans_txt.append(divid_0[1])
				ans_txt.append('')
				val_ans.append(divid_0[0])
			elif tmp[k][0] == '' and tmp[k][1] != '' :
				# Hasil divid index 0 = value index 1 = text
				divid_1 = tmp[k][1].split('^`@`^')

				ans_txt.append('')
				ans_txt.append(divid_1[1])
				val_ans.append(divid_1[0])
			elif tmp[k][0] != '' and tmp[k][1] != '' :
				# Hasil divid index 0 = value index 1 = text
				divid_0 = tmp[k][0].split('^`@`^')
				divid_1 = tmp[k][1].split('^`@`^')

				ans_txt.append(divid_0[1])
				ans_txt.append(divid_1[1])
				val_ans.append(divid_0[0])

		# print('\n',ans_txt,'\n')
		# print('\n',val_ans,'\n')
		answear_txt.append(ans_txt)
		value_ans_btn.append(val_ans)

	return answear_txt, value_ans_btn

			

def run_test (directory) :
	# test = ['e','f','g','h','i','j','k']
	# random.shuffle(test)
	context = ''
	keys = ''
	error = False
	xls_to_list = ''
	try:
		xls = pd.read_excel(directory)
		print(type(xls))
		xls_to_list = xls.values.tolist()
	except Exception as e:
		error = False
		return context, keys, error
	# print(type(xls_to_list))
	# print(len(xls_to_list))
	# print(xls_to_list[0])
	# print(xls_to_list[1])

	# Keterangan ambil data excel
	# indeks baris kolom 0 tidak diambil
	# kolom 1 => jenis soal (1. pilgan, 2. checkbox)
	# kolom 2 => jml opsi jika jenis 2
	# kolom 3 => Kategori soal (untuk di ujikan tidak usah di read)
	# kolom 4 => Soal acak atau tidak. Acak = kumpulkan semua bertipe acak, kemudian acak dengan shuffle
	# 		non acak => kumpulkan dengan non acak, tampilkan terakhir
	# Kolom 5 => data soal
	# Kolom 6 => opsi 1 tip text
	# Kolom 7 => file gambar opsi 1
	# Kolom 8 => opsi 1 tip text
	# Kolom 9 => file gambar opsi 1
	# Kolom 10 => opsi 1 tip text
	# Kolom 11 => file gambar opsi 1
	# Kolom 12 => opsi 1 tip text
	# Kolom 13 => file gambar opsi 1
	# Kolom 14 => opsi 1 tip text
	# Kolom 15 => file gambar opsi 1
	# Kolom 16 Gmabar soal
	# Kolom 17 audio
	# Kolom 18 Video
	# Kolom 19 Kunci jawaban (ditambahkan dengan 5 (+5) misal kunci 2 maka sistem 2+5)
	# Kolom 20 opsi acak jawaban

	row = len(xls_to_list)
	col = len(xls_to_list[0])

	random = []
	non_random = []

	print ('row = ',row,' col = ',col)

	# Memisahkan soal random dan non random
	for x in range(1,row) :
		# soal ti[e acak
		if xls_to_list[x][4] == 'A' :
			random.append(xls_to_list[x])
		# soal tipe non acak
		elif xls_to_list[x][4] == 'T' :
			non_random.append(xls_to_list[x])

	rd.shuffle(random)
	print('\n',len(random),' ',len(non_random),'\n')

	full_quest = random + non_random
	# print(full_quest[0])

	# Di bawah ini adalah var. untuk jadi context
	ans_text, value_ans = answear_view_process(full_quest)
	# print('\n',ans_text,'\n',value_ans,'\n')
	text_quest = []
	type_quest = []
	max_check = []
	img_quest = []
	videos_quest = []
	audio_quest = []
	keys = []
	error = True

	for i in range(len(full_quest)):
		if pd.isna(full_quest[i][5]) == True :
			text_quest.append('')
		else :
			text_quest.append(str(full_quest[i][5]))

		if pd.isna(full_quest[i][1]) == True or full_quest[i][1] > 2:
			type_quest.append('')
			error = False
		else :
			type_quest.append(int(full_quest[i][1]))

		if pd.isna(full_quest[i][2]) == True :
			if type_quest[i] == 2 :
				if int(full_quest[i][1]) == 0 :
					error = False
			max_check.append(0)
		else :
			max_check.append(int(full_quest[i][2]))

		if pd.isna(full_quest[i][16]) == True :
			audio_quest.append('')
		else :
			audio_quest.append(str(full_quest[i][16]))

		if pd.isna(full_quest[i][17]) == True :
			videos_quest.append('')
		else :
			videos_quest.append(str(full_quest[i][17]))

		if pd.isna(full_quest[i][18]) == True :
			img_quest.append('')
		else :
			img_quest.append(str(full_quest[i][18]))

		# Sudah dikoreksi (21-09-2021)
		if pd.isna(full_quest[i][19]) == True :
			keys.append('')
			error = False
		else :
			if_checkbox = ''
			# print('Coba : ','-' in type_quest[i][19],'\n')
			if type_quest[i] == 2 and ('-' in str(full_quest[i][19])) == True:
				ans = str(full_quest[i][19]).split('-')
				keys.append(ans)
				if len(ans) != max_check[i]:
					error = False
			else:
				keys.append(str(int(full_quest[i][19])))

	context = {
		'text_quest' : text_quest,
		'type_quest' : type_quest,
		'ans_txt' : ans_text,
		'val_ans' : value_ans,
		'max_check' : max_check,
		'img_quest' : img_quest,
		'videos_quest' : videos_quest,
		'audio_quest' : audio_quest,
	}

	return context, keys, error
# Ini sudah benar (koreksi tingal jika type checkbox 20 - 09 2021)
def correctionAns(objAnswear, objDataQuest) :
	typeQuest = objDataQuest.getTypeQuest()
	val_quest = 100/objAnswear.get_len()
	ans_keys = objDataQuest.getKeys()
	countVal = 0
	print(type(typeQuest[0]),' ztipe quest ',objAnswear.get_len(),'\n')
	for i in range(objAnswear.get_len()):
		if typeQuest[i] == 1 and len(ans_keys[i]) == 1:
			print(objAnswear.get_list(i),' ',ans_keys,' ',val_quest,'\n')
			if objAnswear.get_list(i) == ans_keys[i] :
				print(countVal,'\n')
				countVal += val_quest
		elif typeQuest[i] == 2 :
			val_quest_multi = val_quest/len(ans_keys[i])
			# Doubel loop untuk cek jawaban multi jawaban
			ans_list = objAnswear.get_list(i)
			for j in range(len(ans_list)):
				for k in range(len(ans_keys[i])):
					if str(ans_list[j]) == str(ans_keys[i][k]):
						print(objAnswear.get_list(i),' ',ans_keys,' ',val_quest_multi,'\n')
						print(countVal,'\n')
						countVal += val_quest_multi
		# Jika admin / guru menginputkan kunci lebih dari satu namun, tipe soal
		# masih pilgan, maka kunci diambil hanya yang index awal.
		elif typeQuest[i] == 1 and len(ans_keys[i]) > 1:
			print(objAnswear.get_list(i),' ',ans_keys,' ',val_quest,'\n')
			if objAnswear.get_list(i) == ans_keys[i][0] :
				print(countVal,'\n')
				countVal += val_quest

	objAnswear.reset()
	objDataQuest.reset()
	return countVal




