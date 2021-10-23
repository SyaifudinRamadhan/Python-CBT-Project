var count = 0;
var page = 0;
let exit = 0;

function addEvent(obj, evt, fn) {
      if (obj.addEventListener) {
          obj.addEventListener(evt, fn, false);
      }
      else if (obj.attachEvent) {
          obj.attachEvent("on" + evt, fn);
      }
}

function check_out(num, p){
  page = p;
  exit = num;
  if (num > 3){
    document.getElementById("submit").click();
    console.log('sudah 3x');
  }
}

addEvent(window,"load",function(e) {
     addEvent(document, "mouseout", function(e) {
        e = e ? e : window.event;
        var from = e.relatedTarget;
        if (!from) {
              // stop your drag event here
              // for now we can just use an alert
            exit = exit + 1;
            alert("Anda sudah keluar "+ exit +" kali");
            count++;
            var url = '/std_test_run?out=xyz';
            
            console.log(page);
            var pss = window.location;
            window.location.href = url;
        }
    });
});

console.log(page);

