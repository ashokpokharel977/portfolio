function toggle () {
	var element = document.getElementById('sidebar');
	element.classList.toggle('sidebar--inactive');
	element.lastElementChild.classList.toggle('hamburger--sticky');
	console.log(element.lastElementChild);
}

var swiper = new Swiper('.swiper-container', {
	effect: 'coverflow',
	grabCursor: true,
	centeredSlides: true,
	slidesPerView: 'auto',
	initialSlide: 1,
	mousewheel: true,
	coverflowEffect: {
		rotate: 50,
		stretch: 0,
		depth: 100,
		modifier: 1,
		slideShadows: true
	},
	pagination: {
		el: '.swiper-pagination'
	},
	breakpoints: {
		// when window width is <= 480px
		480: {
			direction: 'vertical',
			slidesPerView: 1,
			spaceBetween: 30,
			mousewheel: true,
			pagination: {
				el: '.swiper-pagination',
				clickable: true
			}
		}
	}
});

// Get the current breakpoint
var getBreakpoint = function () {
	return window.getComputedStyle(document.body, ':before').content.replace(/\"/g, '');
};

// Get the current breakpoint
var getBreakpoint = function () {
	return window.getComputedStyle(document.body, ':before').content.replace(/\"/g, '');
};

// Recalculate breakpoint on resize
window.addEventListener(
	'resize',
	function () {
		var breakpoint = getBreakpoint();
		if (breakpoint === 'phone') {
			toggle();
		}
	},
	false
);
