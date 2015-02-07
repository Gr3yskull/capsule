$(document).ready(function() {
	var fetched_notes_speed = 200;
	$("#fetched_notes").hide();
	
	$("#fetch").click(function(e) {
		e.preventDefault();
		$.get("fetch/", function(data, status) {
			$("#fetched_notes").html(data);
		}).done(function(){
			$("#fetched_notes").slideDown(fetched_notes_speed);
		});
	});
	
//	$("#fetch").popover()
	$('#element').tooltip('hide');
	$("#fetch_toggle").click(function(e) {
		e.preventDefault();
		$("#fetched_notes").slideUp(fetched_notes_speed);
	});
	
	$("#notes").submit(function(e) {
		e.preventDefault();
		
		data = $("#notes").serialize();
 		$.get("notes/", data, function(data, status) {
 			$("#alert").html(data);
 			$("#status").fadeIn(100);
 			$("#fetch").click();
 		});
	});
})
