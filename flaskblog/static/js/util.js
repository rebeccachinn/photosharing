$(document).ready(function() {
	$('.center-crop-img').each(function(i, obj) {
	    //test
	    if ($(this).height()>$(this).width()){
	    	$(this).addClass("portrait")
	    }
	});
});
