$(document).ready(function(){

	$('.full-success').hide();
	$('.small-success').click(function(){
		$(this).next().slideToggle();
	});

	$('.show-dict-item').hide();
	$('.show-toggle-json').click(function(){
		$(this).next().slideToggle();
	});

	$('.from_to').hide();
	$(".form-vertical .to_radio").hide();


	$(".form-vertical input[type='radio'][name='group1']").change(function(){

		$('.from_to').show();
		$(".form-vertical .to_radio").show();
		$('.from').text($(this).val());
	});

	$(".form-vertical input[type='radio'][name='group2']").change(function(){
		$('.from_to').show();
		$('.to').text($(this).val());
	});

	$(".auth-block-error").click(function () {
	$(this).stop(true,true).fadeOut(800).delay(2500);
	});
});