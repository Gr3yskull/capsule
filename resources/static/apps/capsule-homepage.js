$(document).ready(function() {
	//Activationg functionalities
	$('.carousel').carousel();
	
	//On clicking Login Button
	$("#login-btn").click(function(e) {
		// $('#signup-form-box').hide();
		// $('.modal-backdrop').hide();
		e.preventDefault();
		$('#login-form').removeErrors();
		data = $("#login-form").serializeObject();
 		requestServce("/api/user/login_no_redirect/", data, function(response){
 			if(response['success']) {
 				window.location.href = response['redirect'];
 			} else {
 				$('#login-form').markErrors(response);
 			}
 		});	
	});

	$("#reset-modal").click(function(e) {
		$('#login').click();
		$('#reset').click();
	});

	$("#reset-btn").click(function(e) {
		e.preventDefault();
		$('#reset-form').removeErrors()
		data = $("#reset-form").serializeObject();
		$('#reset-progress-nav').show();
 		requestServce("/api/user/reset_password/", data, function(response){
 			if(response['success']) {
 				$('#reset-progress-nav').hide();
 				$('#close-reset').click();
 				alert("Your password has been successfully reset. Please check your email.");
 				// Perform login
				$('#login').click();
 			} else {
 				$('#reset-progress-nav').hide();
 				$('#reset-form').markErrors(response);
 			}
 		});	
	});

	$("#signup-btn").click(function(e) {
		e.preventDefault();
		$('#signup-form').removeErrors()
		data = $("#signup-form").serializeObject();

		if(validateSignupForm()){
			requestServce("/api/user/signup/", data, function(response){
 				if(response['success']) {
 					alert("You have successfully signed-up. Use your newly created account to login to your new capsule.")
 					$('#close-signup').click();
					// Perform login
					$('#login').click();
 				} else {
 					$('#signup-form').markErrors(response);
 				}
 			});
			
		}
		else
		{
			return false;
		}
	});

	$("#login-btn-redirect").click(function(e) {
		$("#signup-form-box").hide();
		$('.modal-backdrop').hide();
		$("#login").click();
	});

	$("#signup-btn-redirect").click(function(e) {
		$("#login-form-box").hide();
		$('.modal-backdrop').hide();
		$("#signup").click();
	});

	// $("#loginButton").click(function(){
	// 	x=$("loginForm").serializeArray();
	// 	$.post( "server.php",x,function(data) {alert(data);});	// need to change the url, the callback function
	// });

	//On clicking Signup Button
	$("#signupButton").click(function(){

	x=$("signupForm").serializeArray();
			$.post( "server.php",x,function(data) {alert(data);});	// need to change the url, the callback function
		});
});

function handleShortcuts(e) {
	e = e || window.event;
	var charCode = (typeof e.which == "number") ? e.which : e.keyCode;
	if (charCode > 0) {
		// console.log("Code: "+ charCode +", Typed character: " + String.fromCharCode(charCode));
		// If return key is pressed, then,
		if (charCode == 13) {
			var parent = e.target.parentElement
			// Login Form
			if ($(parent).attr('id') == "login-form") {
				console.log('Login proceed');
				$('#login-btn').click();
			// Sigup Form
			} else if ($(parent).attr('id') == "signup-form") {
				console.log('Signup proceed');
				$('#signup-btn').click();
			};
		};
		// Shortcuts
		// `: Perform Login
		if (charCode == 96) {
			console.log('Logging in');
			// First close all other models
			$('#close-signup').click();
			// Perform login
			$('#login').click();
		};
	}
}

// function dummyResponseForUsernameInvalid() {
// 	return {'success': false , 'context': 'signup', 'errors': {
// 		'signup': 'Failed due to invalid form entries.',
// 		'username': 'Username should be at least 4 characters long.'
// 	}};
// }

// function dummyResponseForPasswordLength() {
// 	return {'success': false , 'context': 'signup', 'errors': {
// 		'signup': 'Failed due to invalid form entries.',
// 		'password': 'Password must be at least 6 characters long.'
// 	}};
// }

// function dummyResponseForUsernameInvalidSameAsPassword() {
// 	return {'success': false , 'context': 'signup', 'errors': {
// 		'signup': 'Failed due to invalid form entries.',
// 		'username': 'Password cannot be same as username.'
// 	}};
// }

// function dummyResponseForEmail() {
// 	return {'success': false , 'context': 'signup', 'errors': {
// 		'signup': 'Failed due to invalid form entries.',
// 		'email': 'Enter a valid e-mail address.'
// 	}};
// }

function validateSignupForm() {
	var $form = $('#signup-form');
	var uname = document.forms["signup-form"]["username"].value;
	var pwd = document.forms["signup-form"]["password"].value;
	var mail = document.forms["signup-form"]["email"].value;
	var atpos = mail.indexOf("@");
	var dotpos = mail.lastIndexOf(".");

	if (uname.length < 4 ) {
		$form.markErrors(dummyResponseForUsernameInvalid());
		return false;
	};

	if (pwd.length < 6) {
		$form.markErrors(dummyResponseForPasswordLength());
		return false;
	};

	if (uname == pwd) {
		$form.markErrors(dummyResponseForUsernameInvalidSameAsPassword());
		return false;
	};

	if (!validateConfirmPassword($("#signup-form"))) {
		$form.markErrors(dummyResponseForPasswordsDontMatch());
		return false;
	};

	if (atpos < 1 || dotpos < (atpos+4) || dotpos+2 >= mail.length ) {
		$form.markErrors(dummyResponseForEmail());
		return false;
	};
	
	return true;
}
