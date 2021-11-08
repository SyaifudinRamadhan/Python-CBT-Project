import pandas as pd
import numpy as np

def teach_evaluator(survey_tch_list, result_test_list):
	
	# Keteranngan :
	# Struktur Kolom List survey_tch_list = [ID Guru, Nama, Mapel, kehadiran, ketepatan waktu,
	#          taat aturan, dll sesau draf XLS file example
	# Struktur KOlom list result_test_list = [ID Siswa, Nama siswa, ID Guru mapel, NIlai ujian]

	sorted_list = sorted(survey_tch_list, key = lambda x:x[0]) 
	# for x in range(len(sorted_list)):
	# 	print(sorted_list[x], '\n')

	# Mengumpukan data hasil seleksi
	selection = [] 
	last = ''
	tmp = []
	count = 0
	for x in range(len(sorted_list)): 
		if x == 0:
			last = sorted_list[x][0] 
			tmp = sorted_list[x] 
			count += 1
		else:
			if last == sorted_list[x][0]:
				count += 1
				for y in range(3, len(tmp)):
					tmp[y] += sorted_list[x][y] 
			elif last != sorted_list[x][0]:
				last = sorted_list[x][0] 
				tmp.append(count) 
				selection.append(tmp) 
				tmp = sorted_list[x] 
				count = 1
			if x == (len(sorted_list)-1): 
				tmp.append(count) 
				selection.append(tmp)
	
	# for x in range(len(selection)): 
	# 	print(selection[x])

	# Membuat rata rata skor / poin masing mmasingg guru
	for x in range(len(selection)):
		for y in range(3, len(selection[x])-1):
			selection[x][y] = round(selection[x][y]/selection[x][14]) 

	# for x in range(len(selection)):
	# 	print(selection[x])

	# Mengambil evaluasi dari hasil ujian siswa

	sorted_res_list = sorted(result_test_list, key = lambda x:x[2]) 
	
	# for x in range(len(sorted_res_list)):
	# 	print(sorted_res_list[x], '\n')

	# Menghitung jumlah nilai berdasar interval pada siswa di setiap guru mapelnya
	count_1 = 0;
	count_2 = 0;
	count_3 = 0;
	count_4 = 0;
	count_5 = 0;
	last = ''
	tmp = []
	final_res_data = []
	for x in range(len(sorted_res_list)):
	    if x == 0:
	        last = sorted_res_list[x][2]
	        if sorted_res_list[x][3] <= 20.0:
	            count_1 += 1
	        elif sorted_res_list[x][3] <= 40.0 and sorted_res_list[x][3] > 20.0:
	            count_2 += 1
	        elif sorted_res_list[x][3] <= 60.0 and sorted_res_list[x][3] > 40.0:
	            count_3 += 1
	        elif sorted_res_list[x][3] <= 80.0 and sorted_res_list[x][3] > 60.0:
	            count_4 += 1
	        elif sorted_res_list[x][3] <= 100.0 and sorted_res_list[x][3] > 80.0:
	            count_5 += 1
	        tmp = [sorted_res_list[x][2]]
	        
	    else:
	        if last == sorted_res_list[x][2]:
	            if sorted_res_list[x][3] <= 20.0:
	                count_1 += 1
	            elif sorted_res_list[x][3] <= 40.0 and sorted_res_list[x][3] > 20.0:
	                count_2 += 1
	            elif sorted_res_list[x][3] <= 60.0 and sorted_res_list[x][3] > 40.0:
	                count_3 += 1
	            elif sorted_res_list[x][3] <= 80.0 and sorted_res_list[x][3] > 60.0:
	                count_4 += 1
	            elif sorted_res_list[x][3] <= 100.0 and sorted_res_list[x][3] > 80.0:
	                count_5 += 1
	            
	        elif last != sorted_res_list[x][2]:
	            all_ = count_1+count_2+count_3+count_4+count_5
	            tmp.append(round(count_1/all_*100))
	            tmp.append(round(count_2/all_*100))
	            tmp.append(round(count_3/all_*100))
	            tmp.append(round(count_4/all_*100))
	            tmp.append(round(count_5/all_*100))
	            
	            final_res_data.append(tmp)
	            count_1 = 0
	            count_2 = 0
	            count_3 = 0
	            count_4 = 0
	            count_5 = 0
	            tmp = [sorted_res_list[x][2]]
	            if sorted_res_list[x][3] <= 20.0:
	                count_1 += 1
	            elif sorted_res_list[x][3] <= 40.0 and sorted_res_list[x][3] > 20.0:
	                count_2 += 1
	            elif sorted_res_list[x][3] <= 60.0 and sorted_res_list[x][3] > 40.0:
	                count_3 += 1
	            elif sorted_res_list[x][3] <= 80.0 and sorted_res_list[x][3] > 60.0:
	                count_4 += 1
	            elif sorted_res_list[x][3] <= 100.0 and sorted_res_list[x][3] > 80.0:
	                count_5 += 1
	            last = sorted_res_list[x][2]
	            
	        if x == (len(sorted_res_list)-1):
	            if sorted_res_list[x][3] <= 20.0:
	                count_1 += 1
	            elif sorted_res_list[x][3] <= 40.0 and sorted_res_list[x][3] > 20.0:
	                count_2 += 1
	            elif sorted_res_list[x][3] <= 60.0 and sorted_res_list[x][3] > 40.0:
	                count_3 += 1
	            elif sorted_res_list[x][3] <= 80.0 and sorted_res_list[x][3] > 60.0:
	                count_4 += 1
	            elif sorted_res_list[x][3] <= 100.0 and sorted_res_list[x][3] > 80.0:
	                count_5 += 1
	            all_ =  count_1+count_2+count_3+count_4+count_5
	            tmp.append(round(count_1/all_*100))
	            tmp.append(round(count_2/all_*100))
	            tmp.append(round(count_3/all_*100))
	            tmp.append(round(count_4/all_*100))
	            tmp.append(round(count_5/all_*100))
	            
	            final_res_data.append(tmp)
	            
	# for x in range (len(final_res_data)):
	#     print(final_res_data[x])

	# membuat skor interval 1 - 5 berdasar persentase tersebut
	point = []
	for x in range(len(final_res_data)):
	    if (final_res_data[x][1] > 20.0 or final_res_data[x][2] > 20.0) and (final_res_data[x][4] <= 20.0 and final_res_data[x][5] <= 20.0):
	        point.append([final_res_data[x][0], 1])
	    elif (final_res_data[x][1] > 20.0 or final_res_data[x][2] > 20.0 or final_res_data[x][3] > 20.0) and (final_res_data[x][4] <= 20.0 and final_res_data[x][5] <= 20.0):
	        point.append([final_res_data[x][0], 2])
	    elif (final_res_data[x][1] > 20.0 or final_res_data[x][2] > 20.0 or final_res_data[x][3] > 20.0) and (final_res_data[x][4] <= 20.0 or final_res_data[x][5] <= 20.0):
	        point.append([final_res_data[x][0], 3])
	    elif (final_res_data[x][1] > 20.0 or final_res_data[x][2] > 20.0 or final_res_data[x][3] > 20.0) and (final_res_data[x][4] > 20.0 or final_res_data[x][5] > 20.0):
	        point.append([final_res_data[x][0], 3])
	    elif (final_res_data[x][1] <= 20.0 and final_res_data[x][2] <= 20.0 and final_res_data[x][3] <= 20.0) and (final_res_data[x][4] > 20.0 or final_res_data[x][5] > 20.0):
	        point.append([final_res_data[x][0], 4])
	    elif (final_res_data[x][1] <= 20.0 and final_res_data[x][2] <= 20.0 and final_res_data[x][3] <= 20.0 and final_res_data[x][4] <= 20.0) and (final_res_data[x][5] > 20.0):
	        point.append([final_res_data[x][0], 5])
	        
	    # print(point[x])

	# Mmmberikan bobot dan keputusan akhir
	max_skor = 625
	for x in range(len(selection)):
	    this_skor = 0
	    selection[x][3] = selection[x][3] * 10
	    selection[x][4] = selection[x][4] * 10
	    selection[x][5] = selection[x][5] * 10
	    selection[x][6] = selection[x][6] * 10
	    selection[x][7] = selection[x][7] * 10
	    selection[x][8] = selection[x][8] * 10
	    selection[x][9] = selection[x][9] * 10
	    selection[x][10] = selection[x][10] * 10
	    selection[x][11] = selection[x][11] * 15
	    selection[x][12] = selection[x][12] * 10
	    selection[x][13] = selection[x][13] * 5
	    selection[x][14] = 0
	    for y in range(len(point)):
	        if point[y][0] == selection[x][0]:
	            selection[x][14] = point[y][1] * 15
	    for y in range(3,15):
	        this_skor += selection[x][y]
	    # print(this_skor)
	    this_skor = this_skor/max_skor*100
	    selection[x].append(this_skor)
	    # print(selection[x])

	return selection


def stdn_evaluator(result_test_list):

	sorted_list = sorted(result_test_list, key = lambda x:x[0])
	print(len(sorted_list))
	last = ''
	min_scrore = 75
	tmp = []
	resume = []
	count_plus = 0
	count_min = 0
	for x in range(len(sorted_list)):
		# print(sorted_list[x])
		if x == 0 :
			last = sorted_list[x][0]
			tmp.append(sorted_list[x][0])
			if sorted_list[x][3] < min_scrore:
				count_min += 1
			else:
				count_plus += 1
		else:
			if last == sorted_list[x][0]:
				if sorted_list[x][3] < min_scrore:
					count_min += 1
				else:
					count_plus += 1
			elif last != sorted_list[x][0]:
				tmp.append((count_plus/(count_min+count_plus)*100))
				tmp.append((count_min/(count_min+count_plus)*100))
				tmp.append(sorted_list[x][4])
				resume.append(tmp)
				tmp = []
				count_min = 0
				count_plus = 0

				tmp.append(sorted_list[x][0])
				if sorted_list[x][3] < min_scrore:
					count_min += 1
				else:
					count_plus += 1
				last = sorted_list[x][0]
			if x == len(sorted_list)-1:
				if sorted_list[x][3] < min_scrore:
					count_min += 1
				else:
					count_plus += 1
				tmp.append((count_plus/(count_min+count_plus)*100))
				tmp.append((count_min/(count_min+count_plus)*100))
				tmp.append(sorted_list[x][4])
				resume.append(tmp)

	# for x in range(len(resume)):
	# 	print(resume[x])

	return resume
