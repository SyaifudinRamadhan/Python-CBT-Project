function timeLoad(){
	const today = new Date();
	let h = today.getHours();
	let m = today.getMinutes();
	let s = today.getSeconds();

	document.getElementById("time").innerHTML = today;
	setTimeout(timeLoad, 1000);
}