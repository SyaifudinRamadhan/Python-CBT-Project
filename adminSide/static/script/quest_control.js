function checked_n_fill (now_params, len_pool, this_data){
	if (now_params < len_pool) {
		console.log(this_data[0]);
		if (this_data.length != 0) {
			for (var i = 0; i < this_data.length; i++) {
				// Ini untuk semua radio button
				if ((i > 0 && i <= 4) || i == 20){
					// Khusus no 2 bentuknya isian
					if (i == 2){
						document.getElementById("B").value = this_data[i];
					}else{
						document.getElementById(this_data[i]).checked = true;
					}
				}
				// Ini untuk semua yang isian dan gambar
				else if (i >= 5 && i <= 18 ){
					// Untuk type gambar dan isian yang berdampingan
					if (i >= 6 && i <= 15){
						// Genap untuk indeks bagian isian
						// Ganjil untuk indeks gambar
						if ((i % 2) == 0){
							let elemet = "ans"+(i.toString())
							document.getElementById(elemet).value = this_data[i];
						}else{
							if (this_data[i] !== ''){
								let elemet = "ans_im_"+(i.toString())
								document.getElementById(elemet).src = "/media/"+this_data[i];
							}
						}
					}
					// Hanya ini yanng isian
					else if (i == 5) {
						document.getElementById("E").value=this_data[i];
					}else{
						// Ini semua bertipe file
						console.log(this_data[i]);
						if ( this_data[i] !== '' ){
							let elemet = "file_q_"+(i.toString())
							document.getElementById(elemet).src = "/media/"+this_data[i];
						}
					}
				}
				// Bagian khusus pembuatan kunci jawaban
				else if (i == 19){
					var key = this_data[i].split("-");
					for (var j = 0; j < key.length; j++) {
						var char = "S"+key[j];
						// Ini pengesetan checked sesuai key yang ada
						document.getElementById(char).checked = true;
					}
				}

			}
		}
		else{
			console.log("Datanya kosong broo !!!");
		}
	}
	else{
		console.log("Data tidak ada");
	}
}