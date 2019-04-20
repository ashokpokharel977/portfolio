function toggle () {
	var element = document.getElementById('sidebar');
	element.classList.toggle('sidebar--inactive');
	element.lastElementChild.classList.toggle('hamburger--sticky');
	console.log(element.lastElementChild);
}
function replaceVerticalScrollByHorizontal (event) {
	if (event.deltaY != 0) {
		// manually scroll horizonally instead
		window.scroll(window.scrollX + event.deltaY * 5, window.scrollY);

		// prevent vertical scroll
		event.preventDefault();
	}
	return;
}
// document.getElementById('cards').addEventListener('wheel', replaceVerticalScrollByHorizontal, { passive: false });

var swiper = new Swiper('.project__cards', {
	effect: 'coverflow',
	grabCursor: true,
	centeredSlides: true,
	slidesPerView: 'auto',
	coverflowEffect: {
		rotate: 50,
		stretch: 0,
		depth: 100,
		modifier: 1,
		slideShadows: true
	},
	pagination: {
		el: '.swiper-pagination'
	}
});
