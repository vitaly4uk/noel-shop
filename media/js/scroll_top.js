$(document).ready(function() {
    $("a.on_top-link").hide();
		$(function () {
			$(window).scroll(function () {
				if ($(this).scrollTop() > 50) {
					$('a.on_top-link').fadeIn();
				} else {
					$('a.on_top-link').fadeOut();
				}
			});
			$("a.on_top-link").click(function () { 
		    elementClick = $(this).attr("href");
		    destination = $(elementClick).offset().top;
		    if($.browser.safari){
			  $('body').animate( { scrollTop: destination }, 1100 );
		    }else{
			  $('html').animate( { scrollTop: destination }, 1100 );
		    }
		    return false;
		  });
	    });
	});
