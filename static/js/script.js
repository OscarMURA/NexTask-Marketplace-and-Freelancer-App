(function($) {
	
	"use strict";
	
	
	//Add OnepageNav / Sidebar
	function sideNav() {
		if($('.menu-box .sticky-menu').length){
			$('.menu-box .sticky-menu ul').onePageNav();
		}
	}
	
	//Add Scroll Bar To Sidebar
	if($('#sidebar .menu-box').length){
		$("#sidebar .menu-box").mCustomScrollbar({
			axis:"y",
			autoExpandScrollbar:false
		});
	}
	
	//animate to top on Page Refresh
    $('html, body').animate({
	   scrollTop: $('html, body').offset().top
	}, 1000);

	$('pre.code').highlight();


/* ==========================================================================
   When document is ready, do
   ========================================================================== */
   
	$(document).on('ready', function() {
		sideNav();
	});


})(window.jQuery);



document.querySelector('form').addEventListener('submit', function(event) {
	const startDate = new Date(document.getElementById('id_start_date').value);
	const dueDate = new Date(document.getElementById('id_due_date').value);
	const today = new Date();
	
	if (startDate < today) {
		alert('The start date cannot be in the past.');
		event.preventDefault();
	}

	const minDueDate = new Date(startDate);
	minDueDate.setMonth(minDueDate.getMonth() + 1);

	if (dueDate < minDueDate) {
		alert('The expiration date must be at least one month after the start date.');
		event.preventDefault();
	}

	const budget = document.getElementById('id_budget').value;
	if (budget < 0) {
		alert('The budget cannot be negative.');
		event.preventDefault();
	}
});