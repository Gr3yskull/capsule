$(document).ready(function() {
// Handling form via AJAX
	$("#fader").hover(function() {
		$(this).find("p").fadeIn(200);
	}, function() {
		$(this).find("p").fadeOut(200);
	});
	
	$("#ajaxform").submit(function(e) {
		e.preventDefault();
		
		data = $("#ajaxform").serialize();
		$.get("sc/dat",data, function(data, status) {
    		$("#content").html(data);
		});
	});
	
//	Adding Content to .popovers
	var a = 
		'<div>' +
			'<br />' +
			'<input type="button" class="button" value="Close" onclick="popOverClose()" />' +
		'</div>';
	$('.popover > p').append(a);	
	
//	Resize Event
	$(window).resize(function() {
		$('.popover').find("p").center();
	});
	
//	Popover Registration
	$(".popover > input[type='button']").click(function() {
		var content = $('.popover').find("p");
		
		content.center();
		content.fadeIn(100);
	});
	
//	On click outside the popover region
//	Pending
	
//	Making Key events work
	var triggers = {
		P : 'popover'
	}
	
	$(document).keyup(function(event) {
		var key = String.fromCharCode(event.keyCode);
		if (key in triggers) {
			$(".popover > input[type='button']").click();
		}
	});
	
});

jQuery.fn.center = function () {
    this.css("position","absolute");
    this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) + 
                                                $(window).scrollTop()) + "px");
    this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + 
                                                $(window).scrollLeft()) + "px");
    return this;
}

function popOverV1() {
//	var a = $(this).parent('.popover').innerHTML();
	var content = $('.popover > div').html();
	var canvas = $('.popover_area > div');
	canvas.html(content);
	
	var width = window.innerWidth;
	var height = window.innerHeight;
	var popover = $('.popover_area');
	
	popover.center();
	popover.fadeIn(200);
}


function popOverClose() {
	$('.popover > p').fadeOut(200);
}

function getContent() {
	$("#content").load("def.php");
}

// AJAX Data submission for CSS button
function channelData() {
	data = $("#ajaxform").serialize();
	$.post("def.php",data, function(data, status) {
		$("#content").html(data);
	});
}

// Bogus function
function changeData() {
	var content = document.getElementById("content");
	content.innerHTML = "New Data";
}
