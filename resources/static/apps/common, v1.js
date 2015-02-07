// Credits - http://stackoverflow.com/questions/1184624/convert-form-data-to-js-object-with-jquery
// Last Accessed: 2-Mar-2013
$.fn.serializeObject = function()
{
	var o = {};
	var a = this.serializeArray();
	$.each(a, function() {
		if (o[this.name] !== undefined) {
			if (!o[this.name].push) {
				o[this.name] = [o[this.name]];
			}
			o[this.name].push(this.value || '');
		} else {
			o[this.name] = this.value || '';
		}
	});
	return o;
};

// Credits: http://stackoverflow.com/questions/1208067/wheres-my-json-data-in-my-incoming-django-request
// Last Accessed: 2-Mar-2013
function requestServce(url_request, json_request, callback) {
	$.ajax({
		url: url_request,
		type: 'POST',
		contentType: 'application/json; charset=utf-8',
		data: JSON.stringify(json_request),
		dataType: 'text',
		success: function(result){
			callback(JSON.parse(result))
		}
	});
}

// Credits: http://stackoverflow.com/questions/68485/how-to-show-loading-spinner-in-jquery
// Last Accessed: 2-Mar-2013
$(document).ajaxStart(function() {
	$('#progress-nav').show();
}).ajaxStop(function() {
	$('#progress-nav').hide();
});

$(document).ready(function() {
	$('#progress-nav').hide();
	window.onhashchange = hashBind;
	h = new Highlight();
	// var d = document.getElementById('highlight');
	// $('#highlight').click(h.toggle);
	// d.hide();

	$('#maff').click(function() {
		$('#maff_data').html('Clicked on Maff...');
	});

	$('#mOpenHere').click(function(e) {
		e.preventDefault();
		openTarget(e.target)
	});

	// Highlight Functionality
	// $('#highlight').bind('click.h', addHighlights)
	// $('#highlight').click(removeHighlights)
	// $('#highlight').toggle(addHighlightsStyles, removeHighlightsStyles);


	// $('#highlight').click(function(e) {
	// 	e.preventDefault();
	// 	if (highlight_state == "false") {
	// 		addHighlights(e);
	// 		highlight_state = "true";
	// 		// alert("Added highlight.");
	// 	} else {
	// 		removeHighlights(e);
	// 		highlight_state = "false";
	// 		// alert("Removed highlight.");
	// 	}
	// 	alert(highlight_state);
	// });

	// $('#replace').click(regExApply);
	// $('#remove').click(function() {
	// 	$('.mStyle').each(function(i){
	// 		var html = $(this).html()
	// 		$(this).replaceWith(html)
	// 	});
	// 	$('#replace').toggle();
	// });
	// $('#remove_binding').click(function(){
	// 	$('#replace').off('click');
	// });

	// JSON check
	$('#json_load').click(function(){
		var data =  {
			'name': 'mitthu',
			'age': 20
		};
		requestServce("/json/", data, function(result){
			$("#json-content").html(result['name']);
		});
	});

	$('#replace').click(h.addHighlights);
	$('#remove').click(h.removeHighlights);
	$('#highlight').toggle('click', h.addHighlights, h.removeHighlights);
});

function openTarget(target) {
	var url = target.href;
	$('#app-content').html(iframeWrap(url));
}

function Highlight() {
	this.state = false;
	this.toggle = toggle;
	this.addHighlights = addHighlights;
	this.removeHighlights = removeHighlights;
	this.addHighlightsStyles = addHighlightsStyles;
	this.removeHighlightsStyles = removeHighlightsStyles;

	function toggle(e) {
		e.preventDefault();
		e.stopPropagation();
		if (this.state == false) {
			addHighlights();
			removeHighlightsStyles(e.target);
			this.state = true;
		} else {
			removeHighlights();
			addHighlightsStyles(e.target);
			this.state = false;
		}
	}

	function addHighlights() {
		requestServce("/api/highlights/", "", function(result){
			highlights = result['highlights'];
			highlights.forEach(function(h){
				var re = new RegExp("("+h+")","g");
				var str = $('body').html();
				$('body').html((str.replace(re, '<span class="mStyle">$1</span>')));
			});
		});
	}

	function removeHighlights() {
		// $('.mStyle').each(function(i) {
		// 	var html = $(this).html();
		// 	$(this).replaceWith(html);
		// });
		$('.mStyle').removeClass('mStyle');
	}

	function addHighlightsStyles($target) {
		$($target).removeClass('btn-danger');
		$($target).addClass('btn-success');
		$($target).text('Add Highlights');
	}

	function removeHighlightsStyles($target) {
		$($target).removeClass('btn-success');
		$($target).addClass('btn-danger');
		$($target).text('Remove Highlights');
	}
}
function regExApply(e) {
	e.preventDefault();
	// $(e.target).toggle();
	requestServce("/api/highlights/", "", function(result){
		highlights = result['highlights'];
		highlights.forEach(function(h){
			var re = new RegExp("("+h+")","g");
			var str = $('body').html();
			$('body').html((str.replace(re, '<span class="mStyle">$1</span>')));
		});
	});
}

function objectWrap(url) {
	return  '<object data="'
	+ url
	+ '" '
	+ 'width="100%" height="100%" type="text/html">Object does not exits.'
	+ '</object>'
}

function iframeWrap(url) {
	return  '<iframe src="'
	+ url
	+ '" '
	+ 'width="100%" height="100%">Frame src does not exits.'
	+ '</iframe>'
}

function hashBind() {
	var what_to_do = document.location.hash;

	if (what_to_do == "#wiki")
		openTarget($('#wiki')[0])
}

// var jQ = jQuery.noConflict();
// jQ(document).ready(function() {
//  jQ('#maff').click(function() {
//      jQ('#maff_data').html('Clicked on Maff...');
//  });
//  jQ('#myModal').model('toggle');
// })
