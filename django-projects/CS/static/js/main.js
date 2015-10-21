$(document).ready(function(){ 


	$('.js-btn-get').on('click', function(e){
		e.preventDefault();

		$('#backing, .popup-get').fadeIn(100);

		var temp = $(this).closest('.services-card').attr('data-serv');

		$('#id-services > option').each(function(index, el) {
			if( $(this).attr('data-serv') == temp ) {
				$(this).attr('selected', 'selected');
			}			
		});


	});

	$('#backing, .popup-close').on('click', function(e){
		e.preventDefault();

		$('#backing, .popup').fadeOut(100);

	});


});

Console.log("ok");
