function toggle () {
	var element = document.getElementById('sidebar');
	element.classList.toggle('sidebar--inactive');
	element.lastElementChild.classList.toggle('hamburger--sticky');
	console.log(element.lastElementChild);
}
