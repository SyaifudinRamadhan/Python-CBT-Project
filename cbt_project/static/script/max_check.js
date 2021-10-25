
function checkMaks(num) {
  var checks = document.querySelectorAll(".check");
  // console.log(num,'\n');
  var max = num;
  for (var i = 0; i < checks.length; i++)
    checks[i].onclick = selectiveCheck;
  function selectiveCheck (event) {
    var checkedChecks = document.querySelectorAll(".check:checked");
    if (checkedChecks.length >= max + 1)
      return false;
  }
}

function check(id) {
  console.log(id);
  if (typeof id == 'object'){
    for (var i = 0; i < id.length; i++) {
       if (id[i] === '') {
         console.log('Jawaban kosong')
        }else{
           document.getElementById(id[i]).checked = true;
        }
    }
  }else{
     if (id === '' ) {
        console.log('Jawaban kosong')
      }else{
        document.getElementById(id).checked = true;
      }
  }
}


function pagBtnChange(list){
  for (var i = 0; i < list.length; i++) {
    if (list[i] != '') {
      num = (i+1).toString();
      name = "btn";
      id = name.concat(num);
      console.log(id);
      document.getElementById(id).className = "btn btn-success";
      console.log(i+1)
    }
  }
}
