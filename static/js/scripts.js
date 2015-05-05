$(document).ready(function(){

			$('.list_documents_elements').hide();
			$('.list_documents_line').click(function(){
				$(this).next().slideToggle();
			});
		});