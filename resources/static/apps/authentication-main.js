// Modified on 4-Apr-2013

$(document).ready(function() {
	$("#sign-in").submit(function(e) {
		e.preventDefault();
		data = $("#sign-in").serializeObject();
 		requestServce("/api/user/login_no_redirect/", data, function(response){
 			if(response['success']) {
 				if ($('#redirect')) {
 					window.location.href = $('#redirect').text();
 				} else {
	 				window.location.href = response['redirect'];
 				}
 			} else {
 				$('#sign-in').markErrors(response);
 			}
 		});
	});
})
