// var rows = document.getElementById('table').getElementsByTagName('tr');
function search(id, index_td, table_id){
	// Jalankan live get aearch keyword 
	var keyword  = document.getElementById(id).value;
	// console.log(index_td);
	var filter, table, tr, td, i, txtValue;
		  // input = document.getElementById("myInput");
	filter = keyword.toUpperCase();
	table = document.getElementById(table_id);
	tr = table.getElementsByTagName("tr");
	// console.log(keyword)
		  // Loop through all table rows, and hide those who don't match the search query
	for (i = 0; i < tr.length; i++) {
		td = tr[i].getElementsByTagName("td")[index_td];
		if (td) {
		   txtValue = td.textContent || td.innerText;
		   if (txtValue.toUpperCase().indexOf(filter) > -1) {
		        tr[i].style.display = "";
		    } else {
		        tr[i].style.display = "none";
		    }
		  } 
		}

	if (keyword == ''){
		window.location.reload();
	}

}


// var rows = document.getElementById('table').getElementsByTagName('tr');
// document.getElementById('search').addEventListener('keyup', function (){
// 	var keyword = trim(this.value.replace(/ +/g, ' ')).toLowerCase();
//     console.log(keyword);
    
//       rows.show().filter(function(){
//       	var text = this.text().replace(/\s+/g, ' ').toLowerCase();
//         return !~text.indexOf(keyword);
//       }).hide();
// });